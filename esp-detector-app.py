import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import io

# ESP Detection patterns
ESP_PATTERNS = {
    'Klaviyo': [
        r'klaviyo\.com',
        r'static\.klaviyo\.com',
        r'a\.klaviyo\.com',
        r'klaviyo-account',
        r'klaviyo/klaviyo\.js',
        r'klaviyo\.push',
        r'_learnq'
    ],
    'Mailchimp': [
        r'mailchimp\.com',
        r'list-manage\.com',
        r'mc\.us\d+\.list-manage\.com',
        r'chimpstatic\.com'
    ],
    'Omnisend': [
        r'omnisend\.com',
        r'omnisnippet',
        r'omnisrc'
    ],
    'Attentive': [
        r'attentive\.com',
        r'attn\.tv',
        r'attentivemobile'
    ],
    'Postscript': [
        r'postscript\.io',
        r'pscr\.pt'
    ],
    'Listrak': [
        r'listrak\.com',
        r'listrakbi\.com'
    ],
    'Drip': [
        r'drip\.com',
        r'getdrip\.com'
    ],
    'ActiveCampaign': [
        r'activecampaign\.com',
        r'activehosted\.com'
    ],
    'ConvertKit': [
        r'convertkit\.com',
        r'ck\.page'
    ],
    'Constant Contact': [
        r'constantcontact\.com',
        r'ctctcdn\.com'
    ],
    'Sendinblue': [
        r'sendinblue\.com',
        r'sibautomation',
        r'brevo\.com'
    ],
    'Yotpo': [
        r'yotpo\.com',
        r'staticw2\.yotpo\.com'
    ],
    'Privy': [
        r'privy\.com',
        r'static\.privy\.com'
    ],
    'Justuno': [
        r'justuno\.com',
        r'cjs\.js'
    ],
    'EmailOctopus': [
        r'emailoctopus\.com'
    ],
    'SendGrid': [
        r'sendgrid\.com',
        r'sendgrid\.net'
    ],
    'Mailgun': [
        r'mailgun\.com'
    ],
    'Campaign Monitor': [
        r'createsend\.com',
        r'campaignmonitor\.com'
    ],
    'GetResponse': [
        r'getresponse\.com'
    ],
    'AWeber': [
        r'aweber\.com'
    ]
}

def detect_esp(html_content, url):
    """
    Detect ESP from HTML content
    Returns dict with ESP name and confidence
    """
    detected_esps = {}
    html_lower = html_content.lower()
    
    for esp_name, patterns in ESP_PATTERNS.items():
        matches = 0
        for pattern in patterns:
            if re.search(pattern, html_lower):
                matches += 1
        
        if matches > 0:
            detected_esps[esp_name] = matches
    
    if detected_esps:
        # Return the ESP with most matches
        primary_esp = max(detected_esps, key=detected_esps.get)
        all_esps = ', '.join([f"{esp} ({count})" for esp, count in sorted(detected_esps.items(), key=lambda x: x[1], reverse=True)])
        return primary_esp, all_esps, detected_esps[primary_esp]
    
    return None, None, 0

def fetch_url(url, timeout=10):
    """
    Fetch URL content with proper error handling
    """
    try:
        # Add https:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        
        return response.text, response.url, None
    
    except requests.exceptions.Timeout:
        return None, url, "Timeout"
    except requests.exceptions.ConnectionError:
        return None, url, "Connection Error"
    except requests.exceptions.HTTPError as e:
        return None, url, f"HTTP Error: {e.response.status_code}"
    except Exception as e:
        return None, url, f"Error: {str(e)}"

def process_url(url):
    """
    Process a single URL and detect ESP
    """
    html, final_url, error = fetch_url(url)
    
    if error:
        return {
            'url': url,
            'final_url': final_url,
            'esp': None,
            'all_esps': None,
            'confidence': 0,
            'status': error
        }
    
    primary_esp, all_esps, confidence = detect_esp(html, final_url)
    
    return {
        'url': url,
        'final_url': final_url,
        'esp': primary_esp if primary_esp else 'Not Detected',
        'all_esps': all_esps if all_esps else 'None',
        'confidence': confidence,
        'status': 'Success'
    }

def process_urls_batch(urls, max_workers=5, progress_callback=None):
    """
    Process multiple URLs in parallel
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        
        for i, future in enumerate(as_completed(future_to_url)):
            result = future.result()
            results.append(result)
            
            if progress_callback:
                progress_callback(i + 1, len(urls))
            
            # Small delay to be respectful
            time.sleep(0.1)
    
    return results

# Streamlit UI
st.set_page_config(page_title="ESP Detector", page_icon="📧", layout="wide")

st.title("📧 ESP Detector Tool")
st.markdown("Upload a CSV with URLs to detect Email Service Providers (Klaviyo, Mailchimp, Omnisend, etc.)")

# Sidebar with info
with st.sidebar:
    st.header("About")
    st.markdown("""
    This tool detects Email Service Providers by analyzing website HTML.
    
    **Supported ESPs:**
    - Klaviyo
    - Mailchimp
    - Omnisend
    - Attentive
    - Postscript
    - And 15+ more!
    
    **How to use:**
    1. Upload CSV with 'url' or 'website' column
    2. Click "Detect ESPs"
    3. Download results
    """)
    
    st.header("Settings")
    max_workers = st.slider("Parallel Workers", 1, 10, 5, help="More workers = faster but may trigger rate limits")
    timeout = st.slider("Timeout (seconds)", 5, 30, 10)

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file:
    # Read CSV
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} rows")
        
        # Display preview
        st.subheader("Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Find URL column
        url_column = None
        for col in df.columns:
            if col.lower() in ['url', 'website', 'domain', 'site']:
                url_column = col
                break
        
        if not url_column:
            st.error("❌ No URL column found. Please ensure your CSV has a column named 'url', 'website', 'domain', or 'site'")
        else:
            st.info(f"Using column: **{url_column}**")
            
            # Get URLs
            urls = df[url_column].dropna().unique().tolist()
            st.write(f"Found **{len(urls)}** unique URLs to process")
            
            # Process button
            if st.button("🚀 Detect ESPs", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(current, total):
                    progress = current / total
                    progress_bar.progress(progress)
                    status_text.text(f"Processing: {current}/{total} URLs...")
                
                # Process URLs
                with st.spinner("Detecting ESPs..."):
                    results = process_urls_batch(urls, max_workers=max_workers, progress_callback=update_progress)
                
                # Create results dataframe
                results_df = pd.DataFrame(results)
                
                # Merge with original data
                final_df = df.merge(
                    results_df,
                    left_on=url_column,
                    right_on='url',
                    how='left'
                )
                
                # Display results
                st.success("✅ Processing complete!")
                
                # Stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total URLs", len(results))
                with col2:
                    detected = len([r for r in results if r['esp'] and r['esp'] != 'Not Detected'])
                    st.metric("ESPs Detected", detected)
                with col3:
                    klaviyo_count = len([r for r in results if r['esp'] == 'Klaviyo'])
                    st.metric("Klaviyo Users", klaviyo_count)
                with col4:
                    errors = len([r for r in results if r['status'] != 'Success'])
                    st.metric("Errors", errors)
                
                # ESP breakdown
                st.subheader("ESP Distribution")
                esp_counts = results_df[results_df['esp'] != 'Not Detected']['esp'].value_counts()
                if not esp_counts.empty:
                    st.bar_chart(esp_counts)
                else:
                    st.info("No ESPs detected in this batch")
                
                # Results table
                st.subheader("Results")
                st.dataframe(
                    results_df[['url', 'esp', 'confidence', 'status']],
                    use_container_width=True
                )
                
                # Download button
                csv_buffer = io.StringIO()
                final_df.to_csv(csv_buffer, index=False)
                csv_bytes = csv_buffer.getvalue().encode()
                
                st.download_button(
                    label="📥 Download Results CSV",
                    data=csv_bytes,
                    file_name="esp_detection_results.csv",
                    mime="text/csv"
                )
                
    except Exception as e:
        st.error(f"❌ Error reading CSV: {str(e)}")

# Example section
with st.expander("📝 CSV Format Example"):
    st.markdown("""
    Your CSV should have a column with URLs. Example:
    
    ```csv
    url,company_name
    https://example.com,Example Corp
    example2.com,Another Company
    www.example3.com,Third Company
    ```
    
    The tool will automatically detect columns named: `url`, `website`, `domain`, or `site`
    """)
