"""
HTML parser module - flexible parsing with CSS selectors
"""
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re


class HTMLParser:
    """HTML parser with flexible selector support"""

    def __init__(self, config):
        """Initialize parser

        Args:
            config: Configuration object
        """
        self.config = config
        self.selectors = config.get('selectors', {})

    def parse(self, html: str, url: str) -> Dict[str, Any]:
        """Parse HTML content

        Args:
            html: HTML string
            url: Source URL

        Returns:
            Dictionary of extracted data
        """
        soup = BeautifulSoup(html, 'lxml')

        data = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'title': self._extract_title(soup),
            'meta_description': self._extract_meta_description(soup),
        }

        # Extract data based on configured selectors
        for field_name, selector in self.selectors.items():
            if field_name in ['title', 'meta_description']:
                continue  # Already extracted

            data[field_name] = self._extract_by_selector(soup, selector)

        # Additional extraction methods
        data['links'] = self.extract_links(html, url)
        data['images'] = self.extract_images(soup, url)
        data['text_content'] = self._extract_text(soup)

        return data

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title

        Args:
            soup: BeautifulSoup object

        Returns:
            Page title
        """
        # Try title tag first
        if soup.title:
            title_text = soup.title.get_text(strip=True)
            if title_text:
                return title_text

        # Try h1 tag
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)

        # Try custom selector
        if 'title' in self.selectors:
            title_elem = soup.select_one(self.selectors['title'])
            if title_elem:
                return title_elem.get_text(strip=True)

        return 'No title'

    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description

        Args:
            soup: BeautifulSoup object

        Returns:
            Meta description or empty string
        """
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta['content'].strip()
        return ''

    def _extract_by_selector(self, soup: BeautifulSoup, selector: str) -> List[str]:
        """Extract elements by CSS selector

        Args:
            soup: BeautifulSoup object
            selector: CSS selector

        Returns:
            List of extracted text
        """
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements if elem.get_text(strip=True)]

    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract main text content

        Args:
            soup: BeautifulSoup object

        Returns:
            Cleaned text content
        """
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract all links from page

        Args:
            html: HTML content
            base_url: Base URL for resolving relative links

        Returns:
            List of absolute URLs
        """
        soup = BeautifulSoup(html, 'lxml')
        links = []

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']

            # Skip anchors and javascript
            if href.startswith('#') or href.startswith('javascript:'):
                continue

            # Convert to absolute URL
            absolute_url = urljoin(base_url, href)

            # Validate URL
            if self._is_valid_url(absolute_url):
                links.append(absolute_url)

        return list(set(links))  # Remove duplicates

    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all image URLs

        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative paths

        Returns:
            List of image URLs
        """
        images = []

        for img in soup.find_all('img', src=True):
            src = img['src']
            absolute_url = urljoin(base_url, src)
            images.append(absolute_url)

        return images

    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid

        Args:
            url: URL to check

        Returns:
            True if valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
        except:
            return False

    def extract_structured_data(self, soup: BeautifulSoup, schema: Dict) -> Dict:
        """Extract data based on custom schema

        Args:
            soup: BeautifulSoup object
            schema: Dictionary defining extraction rules

        Returns:
            Extracted structured data
        """
        data = {}

        for field, rule in schema.items():
            if isinstance(rule, str):
                # Simple CSS selector
                data[field] = self._extract_by_selector(soup, rule)
            elif isinstance(rule, dict):
                # Advanced extraction with options
                selector = rule.get('selector')
                attribute = rule.get('attribute')
                regex = rule.get('regex')

                elements = soup.select(selector)

                if attribute:
                    data[field] = [elem.get(attribute) for elem in elements if elem.get(attribute)]
                elif regex:
                    pattern = re.compile(regex)
                    data[field] = [pattern.search(elem.get_text()).group() for elem in elements if pattern.search(elem.get_text())]
                else:
                    data[field] = [elem.get_text(strip=True) for elem in elements]

        return data

    def extract_table_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract data from HTML tables

        Args:
            soup: BeautifulSoup object

        Returns:
            List of dictionaries representing table rows
        """
        tables_data = []

        for table in soup.find_all('table'):
            headers = []
            rows = []

            # Extract headers
            header_row = table.find('tr')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]

            # Extract rows
            for tr in table.find_all('tr')[1:]:
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    if headers and len(headers) == len(cells):
                        rows.append(dict(zip(headers, cells)))
                    else:
                        rows.append({'cells': cells})

            if rows:
                tables_data.append({
                    'headers': headers,
                    'rows': rows
                })

        return tables_data
