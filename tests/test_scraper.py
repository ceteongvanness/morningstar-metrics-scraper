# test_scraper.py
import unittest
from src.scraper import MorningstarScraper

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = MorningstarScraper()

    def test_scrape_ticker(self):
        # Test cases here
        pass