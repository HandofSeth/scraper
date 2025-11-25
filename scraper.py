"""
Web scraper module - handles HTTP requests and page crawling
"""
import requests
import time
from typing import Optional, Set, List
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """Web scraper class for fetching web pages"""

    def __init__(self, config):
        """Initialize scraper

        Args:
            config: Configuration object
        """
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.get_headers())
        self.visited_urls: Set[str] = set()
        self.urls_to_visit: List[str] = []

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a single page

        Args:
            url: URL to fetch

        Returns:
            HTML content or None if failed
        """
        try:
            logger.info(f"Fetching: {url}")

            response = self.session.get(
                url,
                timeout=self.config.get('timeout', 30),
                allow_redirects=True
            )

            if response.status_code == 200:
                logger.info(f"{Fore.GREEN}✓ Success: {url}{Style.RESET_ALL}")
                return response.text
            elif response.status_code == 404:
                logger.warning(f"{Fore.YELLOW}⚠ 404 Not Found: {url}{Style.RESET_ALL}")
                return None
            elif response.status_code == 403:
                logger.warning(f"{Fore.RED}⚠ 403 Forbidden: {url}{Style.RESET_ALL}")
                return None
            else:
                logger.warning(f"{Fore.YELLOW}⚠ Status {response.status_code}: {url}{Style.RESET_ALL}")
                return None

        except requests.exceptions.Timeout:
            logger.error(f"{Fore.RED}✗ Timeout: {url}{Style.RESET_ALL}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"{Fore.RED}✗ Connection Error: {url}{Style.RESET_ALL}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"{Fore.RED}✗ Request failed: {url} - {e}{Style.RESET_ALL}")
            return None
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Unexpected error: {url} - {e}{Style.RESET_ALL}")
            return None

    def crawl(self, start_url: str, max_pages: Optional[int] = None) -> List[dict]:
        """Crawl website starting from URL

        Args:
            start_url: Starting URL
            max_pages: Maximum pages to crawl (None = unlimited)

        Returns:
            List of scraped page data
        """
        from parser import HTMLParser

        parser = HTMLParser(self.config)
        results = []

        self.urls_to_visit = [start_url]
        max_pages = max_pages or self.config.get('max_pages', 10)

        logger.info(f"\n{Fore.CYAN}🚀 Starting crawl from: {start_url}{Style.RESET_ALL}")
        logger.info(f"Max pages: {max_pages}\n")

        while self.urls_to_visit and len(self.visited_urls) < max_pages:
            current_url = self.urls_to_visit.pop(0)

            if current_url in self.visited_urls:
                continue

            if not self._is_allowed_domain(current_url):
                logger.info(f"Skipping (domain not allowed): {current_url}")
                continue

            html = self.fetch_page(current_url)
            self.visited_urls.add(current_url)

            if html:
                # Parse page
                page_data = parser.parse(html, current_url)
                results.append(page_data)

                # Find new links to crawl
                if self.config.get('follow_links', False):
                    new_links = parser.extract_links(html, current_url)
                    self._add_links_to_queue(new_links)

            # Rate limiting
            delay = self.config.get('delay_between_requests', 1)
            if delay > 0 and self.urls_to_visit:
                time.sleep(delay)

        logger.info(f"\n{Fore.GREEN}✓ Crawl complete!{Style.RESET_ALL}")
        logger.info(f"Pages visited: {len(self.visited_urls)}")
        logger.info(f"Pages scraped: {len(results)}\n")

        return results

    def _is_allowed_domain(self, url: str) -> bool:
        """Check if URL domain is allowed

        Args:
            url: URL to check

        Returns:
            True if allowed, False otherwise
        """
        allowed_domains = self.config.get('allowed_domains', [])

        if not allowed_domains:
            return True

        parsed = urlparse(url)
        domain = parsed.netloc

        return any(allowed in domain for allowed in allowed_domains)

    def _add_links_to_queue(self, links: List[str]) -> None:
        """Add new links to crawl queue

        Args:
            links: List of URLs to add
        """
        for link in links:
            if link not in self.visited_urls and link not in self.urls_to_visit:
                self.urls_to_visit.append(link)

    def scrape_single_page(self, url: str) -> Optional[dict]:
        """Scrape a single page without crawling

        Args:
            url: URL to scrape

        Returns:
            Scraped data or None
        """
        from parser import HTMLParser

        parser = HTMLParser(self.config)

        html = self.fetch_page(url)
        if html:
            return parser.parse(html, url)
        return None
