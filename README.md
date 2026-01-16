# 🌐 Universal Web Scraper

A powerful, flexible, and easy-to-use web scraping application built in Python that works with ANY website.

## ✨ Features

- **Universal**: Works with any website through flexible CSS selector configuration
- **Smart Crawling**: Automatically discover and scrape multiple pages
- **Multiple Export Formats**: Save data as JSON, CSV, or both
- **Robust Error Handling**: Handles timeouts, connection errors, and HTTP errors gracefully
- **Rate Limiting**: Built-in delays to avoid overwhelming servers
- **Customizable**: Extensive configuration options via CLI or config files
- **Link Extraction**: Automatically finds and follows links
- **Image Detection**: Extracts all image URLs
- **Clean Data**: Automatic text cleaning and data flattening

## 📦 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python main.py --help
```

## 🚀 Quick Start

### Scrape a Single Page

```bash
python main.py -u https://example.com
```

### Crawl Multiple Pages

```bash
python main.py -u https://example.com --crawl --max-pages 20
```

### Export to CSV

```bash
python main.py -u https://example.com -o csv
```

### Export to Both JSON and CSV

```bash
python main.py -u https://example.com -o both
```

## 📖 Usage Examples

### Basic Examples

```bash
# Scrape a single page with default settings
python main.py -u https://quotes.toscrape.com

# Crawl with custom delay between requests
python main.py -u https://example.com --crawl --delay 3

# Limit crawling to specific domain
python main.py -u https://blog.example.com --crawl --allowed-domains example.com

# Use custom timeout
python main.py -u https://slow-website.com --timeout 60
```

### Advanced Examples with Configuration File

```bash
# Generate example config file
python main.py --generate-config

# Use custom configuration
python main.py --config my_config.json

# Override config with CLI arguments
python main.py --config my_config.json -u https://different-site.com
```

## ⚙️ Configuration

### Command Line Arguments

```
-u, --url              Target URL to scrape
--crawl                Enable crawling (follow links)
--max-pages           Maximum pages to crawl (default: 10)
--delay               Delay between requests in seconds (default: 2)
-o, --output          Output format: json, csv, both (default: json)
--config              Path to configuration JSON file
--generate-config     Generate example configuration file
--selector            CSS selector for specific elements
--timeout             Request timeout in seconds (default: 30)
--allowed-domains     Comma-separated list of allowed domains
```

### Configuration File

Generate an example configuration:

```bash
python main.py --generate-config
```

This creates `scraper_config_example.json`:

```json
{
  "target_url": "https://example.com",
  "max_pages": 10,
  "delay_between_requests": 2,
  "timeout": 30,
  "follow_links": true,
  "max_depth": 3,
  "allowed_domains": [],
  "selectors": {
    "title": "h1",
    "content": "p",
    "links": "a"
  },
  "output_format": "json",
  "output_file": "scraped_data",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "headers": {},
  "export_fields": ["url", "title", "content", "timestamp"]
}
```

### Custom Selectors

Target specific elements using CSS selectors:

```json
{
  "selectors": {
    "title": "h1.article-title",
    "author": ".author-name",
    "date": "time.published",
    "content": "div.article-body p",
    "tags": "a.tag"
  }
}
```

## 📁 Project Structure

```
scraper/
├── main.py              # Entry point with CLI interface
├── scraper.py           # HTTP requests and crawling logic
├── parser.py            # HTML parsing and data extraction
├── storage.py           # Data export (JSON, CSV)
├── config.py            # Configuration management
├── requirements.txt     # Dependencies
├── README.md           # This file
└── output/             # Output directory (created automatically)
    ├── scraped_data_TIMESTAMP.json
    └── scraped_data_TIMESTAMP.csv
```

## 🔧 Customization Guide

### 1. Adapt to a New Website

**Step 1**: Inspect the target website
- Open the website in your browser
- Right-click → Inspect Element
- Find the CSS selectors for the data you want

**Step 2**: Update selectors in config

```json
{
  "target_url": "https://your-target-site.com",
  "selectors": {
    "title": ".post-title",
    "content": ".post-content p",
    "author": ".author-name"
  }
}
```

**Step 3**: Test and adjust

```bash
python main.py --config your_config.json
```

### 2. Add Custom Headers

For websites that require specific headers:

```json
{
  "headers": {
    "Referer": "https://example.com",
    "X-Custom-Header": "value"
  }
}
```

### 3. Handle Pagination

Enable crawling and set allowed domains:

```json
{
  "follow_links": true,
  "allowed_domains": ["example.com"],
  "max_pages": 50
}
```

## 📊 Output Format

### JSON Output

```json
[
  {
    "url": "https://example.com",
    "timestamp": "2025-01-15T10:30:00",
    "title": "Example Page",
    "meta_description": "This is an example",
    "title": ["Main Title"],
    "content": ["Paragraph 1", "Paragraph 2"],
    "links": ["https://example.com/page1", "https://example.com/page2"],
    "images": ["https://example.com/image.jpg"],
    "text_content": "Full page text..."
  }
]
```

### CSV Output

Automatically flattened for easy analysis in Excel or other tools.

## 🛡️ Best Practices

1. **Respect robots.txt**: Check the website's robots.txt file
2. **Use delays**: Always set appropriate delays between requests
3. **Check terms of service**: Ensure you're allowed to scrape the site
4. **Handle errors**: The scraper includes robust error handling
5. **Test first**: Start with a small number of pages
6. **Monitor performance**: Watch for rate limiting or blocks

## ⚠️ Common Issues

### Issue: "Connection Error"

**Solution**: Increase timeout or check internet connection

```bash
python main.py -u https://example.com --timeout 60
```

### Issue: "403 Forbidden"

**Solution**: The site may block scrapers. Try:
- Adjust User-Agent in config
- Add delays between requests
- Check if the site has an API

### Issue: "No data extracted"

**Solution**: CSS selectors may be incorrect
- Inspect the website's HTML structure
- Update selectors in config file
- Test with simple selectors first (e.g., "p", "h1")

## 🔍 Advanced Features

### Extract Table Data

The parser automatically detects and extracts HTML tables.

### Custom Schema Extraction

Use advanced extraction rules in your config:

```json
{
  "selectors": {
    "price": {
      "selector": ".price",
      "attribute": "data-price"
    },
    "rating": {
      "selector": ".rating",
      "regex": "\\d+\\.\\d+"
    }
  }
}
```

## 📝 Examples for Popular Sites

### Example 1: Quotes Website

```bash
python main.py -u https://quotes.toscrape.com --crawl --max-pages 5 -o both
```

### Example 2: News Site

```json
{
  "target_url": "https://news-site.com",
  "selectors": {
    "headline": "h2.headline",
    "summary": "p.summary",
    "author": "span.author",
    "date": "time"
  },
  "follow_links": true,
  "max_pages": 20
}
```

## 🤝 Contributing

Feel free to extend this scraper:
- Add new export formats (XML, SQLite, MongoDB)
- Implement JavaScript rendering (Selenium, Playwright)
- Add proxy support
- Implement authentication handling

## 📄 License

This project is open source and available for educational purposes.

## ⚡ Performance Tips

1. **Parallel requests**: Modify scraper.py to use asyncio for faster crawling
2. **Cache responses**: Add response caching to avoid duplicate requests
3. **Database storage**: Extend storage.py to support databases
4. **Memory optimization**: Process large sites in batches

## 🆘 Support

For issues or questions:
1. Check this README
2. Review the example config
3. Test with simple websites first
4. Check error messages carefully

---


