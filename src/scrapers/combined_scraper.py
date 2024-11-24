# src/scrapers/combined_scraper.py
import time
from typing import Dict, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from ..constants.config import MORNINGSTAR_URL, FINVIZ_URL
from ..utils.logger import setup_logger

class CombinedScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.logger = setup_logger('combined_scraper')

    def scrape_stock_data(self, ticker: str) -> Dict[str, Any]:
        """Scrape stock data from both Morningstar and Finviz"""
        try:
            # Initialize data with ticker
            data = {
                'ticker': ticker,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"\nScraping data for {ticker}...")
            
            # Morningstar URLs
            ms_pages = {
                'quote': f"{MORNINGSTAR_URL}/stocks/{ticker}/quote",
                'dividends': f"{MORNINGSTAR_URL}/stocks/{ticker}/dividends",
                'valuation': f"{MORNINGSTAR_URL}/stocks/{ticker}/valuation",
                'financials': f"{MORNINGSTAR_URL}/stocks/{ticker}/financials"
            }
            
            # Scrape Morningstar data
            ms_data = self._scrape_morningstar(ms_pages)
            data.update(ms_data)
            
            # Finviz URL
            fv_url = f"{FINVIZ_URL}/quote.ashx?t={ticker}"
            
            # Scrape Finviz data
            fv_data = self._scrape_finviz(fv_url)
            data.update(fv_data)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping {ticker}: {str(e)}")
            return self._create_error_data(ticker, str(e))

    def _scrape_morningstar(self, urls: Dict[str, str]) -> Dict[str, Any]:
        """Scrape data from Morningstar"""
        data = {}
        
        try:
            # Get current price
            quote_data = self._scrape_ms_quote(urls['quote'])
            data.update(quote_data)
            
            # Add delay between requests
            time.sleep(2)
            
            # Get dividend data
            dividend_data = self._scrape_ms_dividends(urls['dividends'])
            data.update(dividend_data)
            
            time.sleep(2)
            
            # Get valuation data
            valuation_data = self._scrape_ms_valuation(urls['valuation'])
            data.update(valuation_data)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping Morningstar: {str(e)}")
            return {}

    def _scrape_finviz(self, url: str) -> Dict[str, Any]:
        """Scrape data from Finviz"""
        try:
            response = self._make_request(url)
            if not response:
                return {}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            data = {}
            
            # Scrape Finviz data
            table = soup.find('table', {'class': 'snapshot-table2'})
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    for i in range(0, len(cells), 2):
                        if i + 1 < len(cells):
                            label = cells[i].text.strip()
                            value = cells[i + 1].text.strip()
                            
                            if label == 'Sector':
                                data['sector'] = value
                            elif label == 'Industry':
                                data['industry'] = value
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping Finviz: {str(e)}")
            return {}

    def _scrape_ms_quote(self, url: str) -> Dict[str, Any]:
        """Scrape quote data from Morningstar"""
        try:
            response = self._make_request(url)
            if not response:
                return {}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.select_one('div[data-test="current-price"]')
            
            return {
                'current_price': self._clean_numeric(price_element.text) if price_element else 0.0
            }
        except Exception as e:
            self.logger.error(f"Error scraping Morningstar quote: {str(e)}")
            return {}

    def _scrape_ms_dividends(self, url: str) -> Dict[str, Any]:
        """Scrape dividend data from Morningstar"""
        # Add implementation
        return {}

    def _scrape_ms_valuation(self, url: str) -> Dict[str, Any]:
        """Scrape valuation data from Morningstar"""
        # Add implementation
        return {}

    def _create_error_data(self, ticker: str, error: str) -> Dict[str, Any]:
        """Create data structure for error cases"""
        return {
            'ticker': ticker,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': error,
            'sector': '',
            'industry': '',
            'current_price': 0.0,
            'dividend_ttm': 0.0,
            'yield_5yr_avg': 0.0,
            'bvps_ttm': 0.0,
            'pb_5yr_avg': 0.0,
            'eps_ttm': 0.0,
            'eps_growth': 0.0
        }