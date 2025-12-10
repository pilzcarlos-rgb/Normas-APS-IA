"""
Base scraper class for collecting normative documents.
Implements common functionality for all scrapers.
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper:
    """Base class for web scrapers."""
    
    def __init__(self, base_url: str, delay: float = 1.0):
        """
        Initialize the scraper.
        
        Args:
            base_url: Base URL for the data source
            delay: Delay between requests in seconds
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def get_page(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: URL to fetch
            params: Optional query parameters
        
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            time.sleep(self.delay)
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse date string in various formats.
        
        Args:
            date_str: Date string to parse
        
        Returns:
            datetime object or None if parsing failed
        """
        formats = [
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%d.%m.%Y',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    def save_to_jsonl(self, data: List[Dict], filepath: str):
        """
        Save data to JSONL format.
        
        Args:
            data: List of dictionaries to save
            filepath: Path to output file
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        logger.info(f"Saved {len(data)} items to {filepath}")
    
    def scrape(self) -> List[Dict]:
        """
        Main scraping method to be implemented by subclasses.
        
        Returns:
            List of dictionaries containing scraped data
        """
        raise NotImplementedError("Subclasses must implement scrape()")
