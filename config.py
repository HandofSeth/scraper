"""
Configuration module for the web scraper
"""
import json
from typing import Dict, List, Optional
from pathlib import Path


class Config:
    """Configuration manager for scraper settings"""

    DEFAULT_CONFIG = {
        "target_url": "https://example.com",
        "max_pages": 10,
        "delay_between_requests": 2,
        "timeout": 30,
        "follow_links": True,
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

    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration

        Args:
            config_file: Path to JSON config file (optional)
        """
        self.config = self.DEFAULT_CONFIG.copy()

        if config_file and Path(config_file).exists():
            self.load_from_file(config_file)

    def load_from_file(self, config_file: str) -> None:
        """Load configuration from JSON file

        Args:
            config_file: Path to config file
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                self.config.update(user_config)
        except Exception as e:
            print(f"⚠️  Error loading config file: {e}")
            print("Using default configuration")

    def save_to_file(self, config_file: str) -> None:
        """Save current configuration to JSON file

        Args:
            config_file: Path to save config
        """
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)

    def get(self, key: str, default=None):
        """Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value) -> None:
        """Set configuration value

        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value

    def update(self, updates: Dict) -> None:
        """Update multiple configuration values

        Args:
            updates: Dictionary of updates
        """
        self.config.update(updates)

    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for requests

        Returns:
            Dictionary of headers
        """
        headers = {
            'User-Agent': self.config['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        headers.update(self.config.get('headers', {}))
        return headers

    def __str__(self) -> str:
        """String representation of config"""
        return json.dumps(self.config, indent=2)
