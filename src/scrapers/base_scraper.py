import requests
import time
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from ..utils.logger import setup_logger
from ..constants.config import HEADERS, REQUEST_TIMEOUT, REQUEST_DELAY, MAX_RETRIES

class BaseScraper:
    def __init__(self):
        self.logger = setup_logger('base_scraper')
        self.headers = HEADERS
        self.timeout = REQUEST_TIMEOUT
        self.delay = REQUEST_DELAY
        self.max_retries = MAX_RETRIES

    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                if response.status_code == 200:
                    time.sleep(self.delay)  # Rate limiting
                    return response
                self.logger.warning(f"Request failed with status {response.status_code}")
            except requests.RequestException as e:
                self.logger.error(f"Request attempt {attempt + 1} failed: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
        return None

    def _safe_extract(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Safely extract text from HTML using selector"""
        try:
            element = soup.select_one(selector)
            return element.text.strip() if element else None
        except Exception as e:
            self.logger.error(f"Error extracting element with selector {selector}: {str(e)}")
            return None

    def _clean_numeric(self, value: Optional[str]) -> float:
        """Clean and convert numeric string to float"""
        try:
            if value is None:
                return 0.0
            cleaned = value.replace('$', '').replace(',', '').replace('%', '')
            return float(cleaned)
        except (ValueError, AttributeError):
            return 0.0

    def _create_default_data(self, identifier: str) -> Dict[str, Any]:
        """Create default data structure"""
        return {
            'identifier': identifier,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'error': None
        }