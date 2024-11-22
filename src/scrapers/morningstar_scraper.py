from datetime import datetime
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from ..constants.selectors import SELECTORS, PAGE_URLS

class MorningstarScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.morningstar.com/stocks"

    def scrape_stock_data(self, ticker: str) -> Dict[str, Any]:
        """Scrape financial metrics from Morningstar"""
        try:
            data = self._create_default_data(ticker)
            
            # Scrape from different pages
            pages = {
                'dividends': f"{self.base_url}/{ticker}/dividends",
                'valuation': f"{self.base_url}/{ticker}/valuation",
                'financials': f"{self.base_url}/{ticker}/financials"
            }
            
            # Get data from each page
            dividend_data = self._scrape_dividends_page(pages['dividends'])
            valuation_data = self._scrape_valuation_page(pages['valuation'])
            financial_data = self._scrape_financials_page(pages['financials'])
            
            # Combine all data
            data.update(dividend_data)
            data.update(valuation_data)
            data.update(financial_data)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping {ticker}: {str(e)}")
            return self._create_error_data(ticker, str(e))

    def _scrape_dividends_page(self, url: str) -> Dict[str, Any]:
        """Scrape dividend related metrics"""
        try:
            response = self._make_request(url)
            if not response:
                return {}
                
            soup = BeautifulSoup(response.text, 'html.parser')
            selectors = SELECTORS['dividends']
            
            return {
                'dividend_ttm': self._clean_numeric(self._safe_extract(soup, selectors['dividend_ttm'])),
                'yield_5yr_avg': self._clean_numeric(self._safe_extract(soup, selectors['yield_5yr_avg']))
            }
        except Exception as e:
            self.logger.error(f"Error scraping dividends: {str(e)}")
            return {}

    def _scrape_valuation_page(self, url: str) -> Dict[str, Any]:
        """Scrape valuation metrics"""
        try:
            response = self._make_request(url)
            if not response:
                return {}
                
            soup = BeautifulSoup(response.text, 'html.parser')
            selectors = SELECTORS['valuation']
            
            return {
                'bvps_ttm': self._clean_numeric(self._safe_extract(soup, selectors['bvps_ttm'])),
                'pb_5yr_avg': self._clean_numeric(self._safe_extract(soup, selectors['pb_5yr_avg']))
            }
        except Exception as e:
            self.logger.error(f"Error scraping valuation: {str(e)}")
            return {}

    def _scrape_financials_page(self, url: str) -> Dict[str, Any]:
        """Scrape financial metrics"""
        try:
            response = self._make_request(url)
            if not response:
                return {}
                
            soup = BeautifulSoup(response.text, 'html.parser')
            selectors = SELECTORS['financials']
            
            return {
                'eps_ttm': self._clean_numeric(self._safe_extract(soup, selectors['eps_ttm'])),
                'eps_growth': self._clean_numeric(self._safe_extract(soup, selectors['eps_growth']))
            }
        except Exception as e:
            self.logger.error(f"Error scraping financials: {str(e)}")
            return {}

    def _create_error_data(self, ticker: str, error: str) -> Dict[str, Any]:
        """Create error data structure"""
        return {
            'ticker': ticker,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': error,
            'dividend_ttm': 0.0,
            'yield_5yr_avg': 0.0,
            'bvps_ttm': 0.0,
            'pb_5yr_avg': 0.0,
            'eps_ttm': 0.0,
            'eps_growth': 0.0
        }