# config.py - Configuration settings
MORNINGSTAR_URL = "https://www.morningstar.com/stocks/{ticker}/financials"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
DELAY_BETWEEN_REQUESTS = 2  # seconds

# scraper.py - Main scraping functionality
from bs4 import BeautifulSoup
import requests
from .config import *
from .logger import setup_logger

class MorningstarScraper:
    def __init__(self):
        self.logger = setup_logger()
    
    def scrape_ticker(self, ticker):
        # Scraping logic here
        pass

# utils.py - Helper functions
import pandas as pd
from datetime import datetime

def load_tickers(filepath):
    return pd.read_csv(filepath)

def save_results(data, filename=None):
    if filename is None:
        filename = f'data/output/results_{datetime.now():%Y%m%d_%H%M%S}.csv'
    pd.DataFrame(data).to_csv(filename, index=False)

# logger.py - Logging configuration
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)