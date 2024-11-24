# src/scrapers/base_scraper.py
import requests
from typing import Optional
from ..utils.logger import setup_logger

class BaseScraper:
    def __init__(self):
        self.logger = setup_logger('base_scraper')

    def _make_request(self, url: str) -> Optional[requests.Response]:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            return response if response.status_code == 200 else None
        except Exception as e:
            self.logger.error(f"Error making request to {url}: {str(e)}")
            return None

    def _clean_numeric(self, value: str) -> float:
        """Clean numeric string and convert to float"""
        try:
            # Remove any non-numeric characters except decimal points and minus signs
            cleaned = ''.join(c for c in value if c.isdigit() or c in '.-')
            return float(cleaned)
        except:
            return 0.0