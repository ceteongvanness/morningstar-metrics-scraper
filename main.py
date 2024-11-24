import os
import argparse
from src.scrapers.combined_scraper import CombinedScraper
from src.formatters.csv_formatter import CSVFormatter  # Note: changed from utils to formatters

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Stock data scraper')
    parser.add_argument('--input', required=True, help='Path to input CSV file')
    parser.add_argument('--output', required=True, help='Path to output CSV file')
    args = parser.parse_args()
    
    # Ensure input file exists
    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        return
        
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Initialize components
    try:
        scraper = CombinedScraper()
        formatter = CSVFormatter()
        
        # Read input tickers
        print(f"Reading tickers from {args.input}")
        tickers = formatter.read_input_csv(args.input)
        if not tickers:
            print("No tickers found in input file")
            return
        
        print(f"Found {len(tickers)} tickers")
        
        # Scrape data
        scraped_data = []
        for ticker in tickers:
            print(f"Scraping data for {ticker}...")
            data = scraper.scrape_stock_data(ticker)
            scraped_data.append(data)
            print(f"Completed scraping for {ticker}")
        
        # Format and save data
        if scraped_data:
            print("Formatting data...")
            df = formatter.format_data(scraped_data)
            print(f"Saving data to {args.output}")
            formatter.save_to_csv(df, args.output)
            print("Done!")
        else:
            print("No data was scraped")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()