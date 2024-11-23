from typing import Dict, Any
from bs4 import BeautifulSoup
from datetime import datetime
from .base_scraper import BaseScraper
from ..constants.config import BASE_URL
from ..constants.selectors import SELECTORS

class MorningstarScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.logger = self.logger.getChild('morningstar')

    def scrape_stock_data(self, ticker: str) -> Dict[str, Any]:
        """Scrape stock data from all relevant pages"""
        try:
            data = self._create_default_data(ticker)
            
            # Define page URLs
            pages = {
                'dividends': f"{BASE_URL}/{ticker}/dividends",
                'valuation': f"{BASE_URL}/{ticker}/valuation",
                'financials': f"{BASE_URL}/{ticker}/financials"
            }
            
            # Scrape each page
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
        """Scrape dividend metrics"""
        try:
            response = self._make_request(url)
            if not response:
                return {}
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                'dividend_ttm': self._clean_numeric(
                    self._safe_extract(soup, SELECTORS['dividends']['dividend_ttm'])
                ),
                'yield_5yr_avg': self._clean_numeric(
                    self._safe_extract(soup, SELECTORS['dividends']['yield_5yr_avg'])
                )
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
            
            return {
                'bvps_ttm': self._clean_numeric(
                    self._safe_extract(soup, SELECTORS['valuation']['bvps_ttm'])
                ),
                'pb_5yr_avg': self._clean_numeric(
                    self._safe_extract(soup, SELECTORS['valuation']['pb_5yr_avg'])
                )
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
            
            return {
                'eps_ttm': self._clean_numeric(
                    self._safe_extract(soup, SELECTORS['financials']['eps_ttm'])
                ),
                'eps_growth': self._clean_numeric(
                    self._safe_extract(soup, SELECTORS['financials']['eps_growth'])
                )
            }
        except Exception as e:
            self.logger.error(f"Error scraping financials: {str(e)}")
            return {}

    def _create_error_data(self, ticker: str, error: str) -> Dict[str, Any]:
        """Create data structure for error case"""
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