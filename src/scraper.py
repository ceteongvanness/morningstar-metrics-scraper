import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pandas as pd
import os
from .logger import setup_logger

class MorningstarScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.logger = setup_logger()
        self.base_url = "https://www.morningstar.com/stocks"

    def scrape_stock_data(self, ticker):
        """
        Scrape financial data for a given ticker
        """
        try:
            url = f"{self.base_url}/{ticker}/financials"
            self.logger.info(f"Scraping data for {ticker}")
            
            response = self._make_request(url)
            if not response:
                return self._create_error_dict(ticker, "Failed to get response")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic data
            data = {
                'ticker': ticker,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                **self._extract_financial_data(soup)
            }
            
            # Calculate metrics
            metrics = self._calculate_metrics(data)
            data.update(metrics)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping {ticker}: {str(e)}")
            return self._create_error_dict(ticker, str(e))

    def _make_request(self, url):
        """
        Make HTTP request with retry logic
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    return response
                time.sleep(2 ** attempt)  # Exponential backoff
            except requests.RequestException as e:
                self.logger.warning(f"Request attempt {attempt + 1} failed: {str(e)}")
        return None

    def _extract_financial_data(self, soup):
        """
        Extract financial data from BeautifulSoup object
        """
        try:
            # Replace these selectors with actual ones from Morningstar
            dividend = self._safe_extract(soup, 'div.dividend-value')
            price = self._safe_extract(soup, 'div.price-value')
            pb_ratio = self._safe_extract(soup, 'div.pb-ratio')
            pe_ratio = self._safe_extract(soup, 'div.pe-ratio')
            growth_rate = self._safe_extract(soup, 'div.growth-rate')
            
            return {
                'dividend_per_share': dividend,
                'current_price': price,
                'pb_ratio': pb_ratio,
                'pe_ratio': pe_ratio,
                'growth_rate': growth_rate
            }
        except Exception as e:
            self.logger.error(f"Error extracting financial data: {str(e)}")
            return {}

    def _safe_extract(self, soup, selector):
        """
        Safely extract and convert value from HTML
        """
        try:
            element = soup.select_one(selector)
            if element:
                value = element.text.strip()
                # Remove currency symbols and convert to float
                value = value.replace('$', '').replace(',', '')
                return float(value)
        except Exception:
            return None
        return None

    def _calculate_metrics(self, data):
        """
        Calculate financial metrics based on extracted data
        """
        try:
            metrics = {}
            
            # Target Yield Rate
            if data.get('dividend_per_share') and data.get('current_price'):
                metrics['target_yield_rate'] = data['dividend_per_share'] / (data['current_price'] * 1.2)
            
            # Relative P/B
            if data.get('pb_ratio') and data.get('book_value'):
                metrics['relative_pb'] = data['pb_ratio'] * data['book_value']
            
            # PEG Growth
            if data.get('pe_ratio') and data.get('growth_rate'):
                metrics['peg_growth'] = data['pe_ratio'] * data['growth_rate'] * 100
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {str(e)}")
            return {}

    def _create_error_dict(self, ticker, error_message):
        """
        Create standardized error dictionary
        """
        return {
            'ticker': ticker,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': error_message
        }