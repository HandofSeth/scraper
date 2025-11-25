"""
Storage module - handles data export to various formats
"""
import json
import csv
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataStorage:
    """Data storage and export handler"""

    def __init__(self, config):
        """Initialize storage

        Args:
            config: Configuration object
        """
        self.config = config
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)

    def save(self, data: List[Dict[str, Any]], format: str = None) -> str:
        """Save data in specified format

        Args:
            data: List of dictionaries to save
            format: Output format ('json', 'csv', or 'both')

        Returns:
            Path to saved file(s)
        """
        if not data:
            logger.warning("No data to save")
            return ""

        format = format or self.config.get('output_format', 'json')
        base_filename = self.config.get('output_file', 'scraped_data')

        saved_files = []

        if format in ['json', 'both']:
            json_file = self.save_json(data, base_filename)
            saved_files.append(json_file)

        if format in ['csv', 'both']:
            csv_file = self.save_csv(data, base_filename)
            saved_files.append(csv_file)

        return ', '.join(saved_files)

    def save_json(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Save data as JSON

        Args:
            data: Data to save
            filename: Base filename

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = self.output_dir / f"{filename}_{timestamp}.json"

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"✓ JSON saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"✗ Error saving JSON: {e}")
            return ""

    def save_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Save data as CSV

        Args:
            data: Data to save
            filename: Base filename

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = self.output_dir / f"{filename}_{timestamp}.csv"

        try:
            # Flatten nested data for CSV
            flat_data = self._flatten_data(data)

            if not flat_data:
                logger.warning("No data to write to CSV")
                return ""

            # Get all unique keys
            fieldnames = set()
            for row in flat_data:
                fieldnames.update(row.keys())

            fieldnames = sorted(list(fieldnames))

            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(flat_data)

            logger.info(f"✓ CSV saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"✗ Error saving CSV: {e}")
            return ""

    def _flatten_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten nested data structures for CSV export

        Args:
            data: Data to flatten

        Returns:
            Flattened data
        """
        flattened = []

        for item in data:
            flat_item = {}

            for key, value in item.items():
                if isinstance(value, (list, tuple)):
                    # Convert lists to comma-separated strings
                    flat_item[key] = ', '.join(str(v) for v in value if v)
                elif isinstance(value, dict):
                    # Flatten nested dictionaries
                    for sub_key, sub_value in value.items():
                        flat_item[f"{key}_{sub_key}"] = sub_value
                else:
                    flat_item[key] = value

            flattened.append(flat_item)

        return flattened

    def save_raw_html(self, html: str, url: str) -> str:
        """Save raw HTML content

        Args:
            html: HTML content
            url: Source URL

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = self._sanitize_filename(url)
        filepath = self.output_dir / f"html_{safe_filename}_{timestamp}.html"

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

            logger.info(f"✓ HTML saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"✗ Error saving HTML: {e}")
            return ""

    def _sanitize_filename(self, text: str) -> str:
        """Create safe filename from text

        Args:
            text: Text to sanitize

        Returns:
            Safe filename string
        """
        import re
        # Remove or replace unsafe characters
        safe = re.sub(r'[^\w\s-]', '', text)
        safe = re.sub(r'[-\s]+', '_', safe)
        return safe[:50]  # Limit length

    def append_to_json(self, data: Dict[str, Any], filename: str) -> bool:
        """Append data to existing JSON file

        Args:
            data: Data to append
            filename: Target filename

        Returns:
            True if successful, False otherwise
        """
        filepath = self.output_dir / filename

        try:
            existing_data = []

            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)

            existing_data.append(data)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            logger.error(f"✗ Error appending to JSON: {e}")
            return False

    def get_export_summary(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics of scraped data

        Args:
            data: Scraped data

        Returns:
            Summary statistics
        """
        if not data:
            return {
                'total_pages': 0,
                'total_links': 0,
                'total_images': 0
            }

        total_links = sum(len(item.get('links', [])) for item in data)
        total_images = sum(len(item.get('images', [])) for item in data)

        return {
            'total_pages': len(data),
            'total_links': total_links,
            'total_images': total_images,
            'pages': [
                {
                    'url': item.get('url'),
                    'title': item.get('title'),
                    'timestamp': item.get('timestamp')
                }
                for item in data
            ]
        }
