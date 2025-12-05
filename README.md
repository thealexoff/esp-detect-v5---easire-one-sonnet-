# 📧 ESP Detector Tool

A Streamlit web application that detects Email Service Providers (ESPs) from website URLs by analyzing HTML content.

## 🚀 Features

- **Batch Processing**: Upload CSV files with multiple URLs
- **20+ ESP Detection**: Detects Klaviyo, Mailchimp, Omnisend, Attentive, Postscript, and 15+ more
- **Parallel Processing**: Configurable multi-threading for faster results
- **Confidence Scoring**: Shows how many detection patterns matched
- **Visual Dashboard**: Bar charts and metrics for quick insights
- **CSV Export**: Download results with all original data preserved
- **Error Handling**: Graceful handling of timeouts, connection errors, etc.

## 📊 Supported ESPs

- Klaviyo
- Mailchimp
- Omnisend
- Attentive
- Postscript
- Listrak
- Drip
- ActiveCampaign
- ConvertKit
- Constant Contact
- Sendinblue/Brevo
- Yotpo
- Privy
- Justuno
- EmailOctopus
- SendGrid
- Mailgun
- Campaign Monitor
- GetResponse
- AWeber

## 🛠️ Installation

### Local Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/esp-detector.git
cd esp-detector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run esp_detector_app.py
```

4. Open your browser to `http://localhost:8501`

### Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and `esp_detector_app.py`
5. Click "Deploy"

## 📝 Usage

1. **Prepare your CSV file** with URLs:
   - Must have a column named: `url`, `website`, `domain`, or `site`
   - URLs can be in any format: `example.com`, `www.example.com`, or `https://example.com`

2. **Upload the CSV** in the Streamlit interface

3. **Configure settings** (optional):
   - Parallel Workers: More workers = faster processing (but may trigger rate limits)
   - Timeout: How long to wait for each website to respond

4. **Click "Detect ESPs"** and wait for results

5. **Download results** as CSV with all ESP detection data

## 📁 CSV Format Example

```csv
url,company_name,industry
https://example.com,Example Corp,ecommerce
example2.com,Another Company,beauty
www.example3.com,Third Company,fashion
```

## 🔧 How It Works

The tool:
1. Fetches HTML content from each URL
2. Searches for ESP-specific patterns (JavaScript snippets, tracking pixels, form endpoints)
3. Counts pattern matches for confidence scoring
4. Returns primary ESP and all detected ESPs

Detection patterns include:
- JavaScript tracking pixels
- Email signup form endpoints
- Third-party script URLs
- Cookie scripts
- Meta tags and identifiers

## ⚙️ Configuration

Edit `ESP_PATTERNS` in `esp_detector_app.py` to:
- Add new ESPs
- Modify detection patterns
- Adjust confidence scoring

## 🤝 Contributing

Pull requests welcome! To add support for a new ESP:

1. Find their tracking/integration code patterns
2. Add to `ESP_PATTERNS` dictionary
3. Test with known sites using that ESP
4. Submit PR

## 📄 License

MIT License - feel free to use for commercial purposes

## 🐛 Known Limitations

- Cannot detect ESPs that only use server-side integrations
- Some sites block automated requests (will show as errors)
- Rate limiting may occur with very large batches
- Requires publicly accessible websites

## 💡 Tips

- Start with 5 parallel workers for best balance of speed/reliability
- For large batches (1000+ URLs), consider running overnight
- Check error rows - they may need manual verification
- Klaviyo users often have multiple pattern matches (high confidence)

## 📧 Contact

Built for DTC ecommerce lead generation.

---

**Star this repo if you find it useful!** ⭐
