# main.py
from src.scraper import MorningstarScraper
from src.utils import load_tickers, save_results
import argparse

def main():
    parser = argparse.ArgumentParser(description='Morningstar Data Scraper')
    parser.add_argument('--input', default='data/input/tickers.csv',
                      help='Path to input CSV file')
    parser.add_argument('--output', 
                      help='Path to output CSV file (optional)')
    args = parser.parse_args()

    # Initialize scraper
    scraper = MorningstarScraper()
    
    # Load tickers
    tickers = load_tickers(args.input)
    
    # Process each ticker
    results = []
    for ticker in tickers['Ticker']:
        result = scraper.scrape_ticker(ticker)
        results.append(result)
    
    # Save results
    save_results(results, args.output)

if __name__ == '__main__':
    main()