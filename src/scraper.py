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
            # We'll need to access multiple pages to get all data
            financials_url = f"{self.base_url}/{ticker}/financials"
            valuation_url = f"{self.base_url}/{ticker}/valuation"
            dividends_url = f"{self.base_url}/{ticker}/dividends"
            
            self.logger.info(f"Scraping data for {ticker}")
            
            data = {
                'ticker': ticker,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Get dividend data (K3: 股息TTM)
            dividend_data = self._get_dividend_data(dividends_url)
            data.update(dividend_data)
            
            # Get historical yield data (L3: 近5年平均殖利率)
            yield_data = self._get_historical_yield(dividends_url)
            data.update(yield_data)
            
            # Get BVPS data (M3: BVPS TTM)
            bvps_data = self._get_bvps_data(financials_url)
            data.update(bvps_data)
            
            # Get historical P/B data (N3: 近5年平均P/B)
            pb_data = self._get_historical_pb(valuation_url)
            data.update(pb_data)
            
            # Get EPS data (O3: EPS TTM)
            eps_data = self._get_eps_data(financials_url)
            data.update(eps_data)
            
            # Get EPS growth rate (P3: EPS成長率%)
            growth_data = self._get_eps_growth(financials_url)
            data.update(growth_data)
            
            # Calculate metrics
            metrics = self._calculate_metrics(data)
            data.update(metrics)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping {ticker}: {str(e)}")
            return self._create_error_dict(ticker, str(e))

    def _get_dividend_data(self, url):
        """Get TTM Dividend (K3)"""
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                dividend = self._safe_extract(soup, 'div[data-test="dividend-ttm"]')
                return {'dividend_ttm': dividend}
        except Exception as e:
            self.logger.error(f"Error getting dividend data: {str(e)}")
        return {'dividend_ttm': None}

    def _get_historical_yield(self, url):
        """Get 5-year Average Yield (L3)"""
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                yield_avg = self._safe_extract(soup, 'div[data-test="yield-5year-avg"]')
                return {'yield_5year_avg': yield_avg}
        except Exception as e:
            self.logger.error(f"Error getting yield data: {str(e)}")
        return {'yield_5year_avg': None}

    def _get_bvps_data(self, url):
        """Get BVPS TTM (M3)"""
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                bvps = self._safe_extract(soup, 'div[data-test="bvps-ttm"]')
                return {'bvps_ttm': bvps}
        except Exception as e:
            self.logger.error(f"Error getting BVPS data: {str(e)}")
        return {'bvps_ttm': None}

    def _get_historical_pb(self, url):
        """Get 5-year Average P/B (N3)"""
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                pb_avg = self._safe_extract(soup, 'div[data-test="pb-5year-avg"]')
                return {'pb_5year_avg': pb_avg}
        except Exception as e:
            self.logger.error(f"Error getting P/B data: {str(e)}")
        return {'pb_5year_avg': None}

    def _get_eps_data(self, url):
        """Get EPS TTM (O3)"""
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                eps = self._safe_extract(soup, 'div[data-test="eps-ttm"]')
                return {'eps_ttm': eps}
        except Exception as e:
            self.logger.error(f"Error getting EPS data: {str(e)}")
        return {'eps_ttm': None}

    def _get_eps_growth(self, url):
        """Get EPS Growth Rate (P3)"""
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                growth = self._safe_extract(soup, 'div[data-test="eps-growth"]')
                return {'eps_growth': growth}
        except Exception as e:
            self.logger.error(f"Error getting EPS growth data: {str(e)}")
        return {'eps_growth': None}

    def _calculate_metrics(self, data):
        """
        Calculate the three required metrics:
        1. 目標殖利率 = K3/(L3*1.2)
        2. 相對 P/B = M3*N3
        3. PEG 成長股 = O3*P3*100
        """
        try:
            metrics = {}
            
            # 目標殖利率
            if data.get('dividend_ttm') and data.get('yield_5year_avg'):
                metrics['target_yield'] = data['dividend_ttm'] / (data['yield_5year_avg'] * 1.2)
            
            # 相對 P/B
            if data.get('bvps_ttm') and data.get('pb_5year_avg'):
                metrics['relative_pb'] = data['bvps_ttm'] * data['pb_5year_avg']
            
            # PEG 成長股
            if data.get('eps_ttm') and data.get('eps_growth'):
                metrics['peg_growth'] = data['eps_ttm'] * data['eps_growth'] * 100
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {str(e)}")
            return {}

    def _make_request(self, url):
        """Make HTTP request with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    return response
                time.sleep(2 ** attempt)
            except requests.RequestException as e:
                self.logger.warning(f"Request attempt {attempt + 1} failed: {str(e)}")
        return None

    def _safe_extract(self, soup, selector):
        """Safely extract and convert value from HTML"""
        try:
            element = soup.select_one(selector)
            if element:
                value = element.text.strip()
                value = value.replace('$', '').replace(',', '').replace('%', '')
                return float(value)
        except Exception:
            return None
        return None

    def _create_error_dict(self, ticker, error_message):
        """Create standardized error dictionary"""
        return {
            'ticker': ticker,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': error_message,
            'dividend_ttm': None,           # K3
            'yield_5year_avg': None,        # L3
            'bvps_ttm': None,              # M3
            'pb_5year_avg': None,          # N3
            'eps_ttm': None,               # O3
            'eps_growth': None,            # P3
            'target_yield': None,          # K3/(L3*1.2)
            'relative_pb': None,           # M3*N3
            'peg_growth': None             # O3*P3*100
        }