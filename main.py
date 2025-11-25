#!/usr/bin/env python3
"""
Universal Web Scraper - Main Entry Point
A flexible, configurable web scraper that works with any website
"""
import argparse
import sys
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

from config import Config
from scraper import WebScraper
from storage import DataStorage


def print_banner():
    """Print application banner"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════╗
║                                                   ║
║        🌐  UNIVERSAL WEB SCRAPER  🌐            ║
║                                                   ║
║     Flexible scraper for any website             ║
║                                                   ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)


def parse_arguments():
    """Parse command line arguments

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Universal Web Scraper - Scrape any website with ease',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape single page
  python main.py -u https://example.com

  # Crawl entire site (max 50 pages)
  python main.py -u https://example.com --crawl --max-pages 50

  # Use custom config file
  python main.py --config my_config.json

  # Export to both CSV and JSON
  python main.py -u https://example.com -o both

  # Generate example config
  python main.py --generate-config
        """
    )

    parser.add_argument(
        '-u', '--url',
        help='Target URL to scrape',
        type=str
    )

    parser.add_argument(
        '--crawl',
        help='Crawl multiple pages (follow links)',
        action='store_true'
    )

    parser.add_argument(
        '--max-pages',
        help='Maximum pages to crawl (default: 10)',
        type=int,
        default=10
    )

    parser.add_argument(
        '--delay',
        help='Delay between requests in seconds (default: 2)',
        type=float,
        default=2
    )

    parser.add_argument(
        '-o', '--output',
        help='Output format: json, csv, or both (default: json)',
        choices=['json', 'csv', 'both'],
        default='json'
    )

    parser.add_argument(
        '--config',
        help='Path to configuration JSON file',
        type=str
    )

    parser.add_argument(
        '--generate-config',
        help='Generate example configuration file',
        action='store_true'
    )

    parser.add_argument(
        '--selector',
        help='CSS selector for specific elements (e.g., "h2.title")',
        type=str
    )

    parser.add_argument(
        '--timeout',
        help='Request timeout in seconds (default: 30)',
        type=int,
        default=30
    )

    parser.add_argument(
        '--allowed-domains',
        help='Comma-separated list of allowed domains for crawling',
        type=str
    )

    return parser.parse_args()


def generate_example_config():
    """Generate example configuration file"""
    config = Config()
    config_path = 'scraper_config_example.json'
    config.save_to_file(config_path)

    print(f"{Fore.GREEN}✓ Example configuration generated: {config_path}{Style.RESET_ALL}")
    print(f"\nEdit this file and use: python main.py --config {config_path}")


def main():
    """Main application entry point"""
    print_banner()

    args = parse_arguments()

    # Generate config if requested
    if args.generate_config:
        generate_example_config()
        return

    # Validate URL
    if not args.url and not args.config:
        print(f"{Fore.RED}✗ Error: Please provide a URL with -u or a config file with --config{Style.RESET_ALL}")
        print(f"Use: python main.py --help for usage information")
        sys.exit(1)

    try:
        # Load configuration
        config = Config(args.config) if args.config else Config()

        # Override config with command line arguments
        if args.url:
            config.set('target_url', args.url)

        if args.max_pages:
            config.set('max_pages', args.max_pages)

        if args.delay:
            config.set('delay_between_requests', args.delay)

        if args.output:
            config.set('output_format', args.output)

        if args.timeout:
            config.set('timeout', args.timeout)

        if args.allowed_domains:
            domains = [d.strip() for d in args.allowed_domains.split(',')]
            config.set('allowed_domains', domains)

        if args.crawl:
            config.set('follow_links', True)

        if args.selector:
            config.config['selectors']['custom'] = args.selector

        # Display configuration
        print(f"{Fore.CYAN}📋 Configuration:{Style.RESET_ALL}")
        print(f"  Target URL: {config.get('target_url')}")
        print(f"  Max pages: {config.get('max_pages')}")
        print(f"  Crawl mode: {'Enabled' if config.get('follow_links') else 'Disabled'}")
        print(f"  Output format: {config.get('output_format')}")
        print(f"  Delay: {config.get('delay_between_requests')}s")
        print()

        # Initialize components
        scraper = WebScraper(config)
        storage = DataStorage(config)

        # Scrape data
        target_url = config.get('target_url')

        if config.get('follow_links'):
            print(f"{Fore.CYAN}🕷️  Starting crawler...{Style.RESET_ALL}\n")
            results = scraper.crawl(target_url, config.get('max_pages'))
        else:
            print(f"{Fore.CYAN}📄 Scraping single page...{Style.RESET_ALL}\n")
            result = scraper.scrape_single_page(target_url)
            results = [result] if result else []

        # Save results
        if results:
            print(f"\n{Fore.CYAN}💾 Saving data...{Style.RESET_ALL}")

            saved_files = storage.save(results, config.get('output_format'))

            # Display summary
            summary = storage.get_export_summary(results)

            print(f"\n{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Scraping Complete!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}\n")

            print(f"📊 Summary:")
            print(f"  Pages scraped: {summary['total_pages']}")
            print(f"  Links found: {summary['total_links']}")
            print(f"  Images found: {summary['total_images']}")
            print(f"\n📁 Output files: {saved_files}")

            print(f"\n{Fore.CYAN}Done!{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}⚠️  No data was scraped{Style.RESET_ALL}")

    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️  Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
