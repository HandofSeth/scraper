# 🚀 Quick Start Guide

## Installation (2 minutes)

### Step 1: Install Dependencies

```bash
cd scraper
pip install -r requirements.txt
```

### Step 2: Test Installation

```bash
python main.py --help
```

## Usage Examples

### 1️⃣ Scrape a Single Page

```bash
python main.py -u https://quotes.toscrape.com
```

**Output**: Creates `output/scraped_data_TIMESTAMP.json`

### 2️⃣ Crawl Multiple Pages

```bash
python main.py -u https://quotes.toscrape.com --crawl --max-pages 5
```

**Output**: Follows links and scrapes up to 5 pages

### 3️⃣ Export to CSV

```bash
python main.py -u https://example.com -o csv
```

**Output**: Creates `output/scraped_data_TIMESTAMP.csv`

### 4️⃣ Export to Both JSON and CSV

```bash
python main.py -u https://example.com -o both
```

### 5️⃣ Use Example Configuration

```bash
python main.py --config example_config.json
```

## Customize for Your Website

### Step 1: Inspect the Website

1. Open your target website in a browser
2. Right-click on an element you want to scrape
3. Select "Inspect" or "Inspect Element"
4. Note the CSS selector (e.g., `.article-title`, `h2.post-heading`)

### Step 2: Create Config File

```bash
python main.py --generate-config
```

Edit `scraper_config_example.json`:

```json
{
  "target_url": "https://your-site.com",
  "selectors": {
    "title": "h1.page-title",
    "content": "div.article-body p",
    "author": ".author-name"
  },
  "max_pages": 10,
  "output_format": "both"
}
```

### Step 3: Run with Your Config

```bash
python main.py --config scraper_config_example.json
```

## Common Use Cases

### Scrape Blog Posts

```json
{
  "target_url": "https://blog.example.com",
  "selectors": {
    "title": "h1.post-title",
    "date": "time.published",
    "author": ".author",
    "content": ".post-content p"
  },
  "follow_links": true,
  "max_pages": 20
}
```

### Scrape Product Listings

```json
{
  "target_url": "https://shop.example.com/products",
  "selectors": {
    "product_name": ".product-title",
    "price": ".product-price",
    "description": ".product-description",
    "rating": ".rating"
  },
  "max_pages": 50
}
```

### Scrape News Articles

```json
{
  "target_url": "https://news.example.com",
  "selectors": {
    "headline": "h2.headline",
    "summary": "p.summary",
    "category": ".category",
    "timestamp": "time"
  },
  "follow_links": true
}
```

## Tips

✅ **Start small**: Test with 1-2 pages first
✅ **Use delays**: Respect the server with `--delay 2`
✅ **Check robots.txt**: Visit `https://site.com/robots.txt`
✅ **Verify output**: Check the output folder after each run
✅ **Adjust selectors**: If no data is extracted, update CSS selectors

## Troubleshooting

**No data extracted?**
- Verify CSS selectors by inspecting the page
- Try simpler selectors like `p`, `h1`, `div`

**Connection errors?**
- Increase timeout: `--timeout 60`
- Check your internet connection

**403 Forbidden?**
- The site may block scrapers
- Try adjusting the User-Agent in config
- Check site's terms of service

## Next Steps

📚 Read the full [README.md](README.md) for advanced features
⚙️ Explore configuration options
🎯 Customize for your specific needs

**Happy Scraping!** 🌐
