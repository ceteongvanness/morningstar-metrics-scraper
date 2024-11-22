import pandas as pd
import os
import argparse
from datetime import datetime
from src.scraper import MorningstarScraper
from src.utils import ensure_directory_exists

def parse_arguments():
    parser = argparse.ArgumentParser(description='Morningstar Data Scraper')
    parser.add_argument('--input', 
                      default='data/input/tickers.csv',
                      help='Path to input CSV file')
    parser.add_argument('--output',
                      help='Path to output CSV file (optional)')
    parser.add_argument('--delay',
                      type=int,
                      default=2,
                      help='Delay between requests in seconds')
    return parser.parse_args()

def load_tickers(filepath):
    """
    Load tickers from CSV file
    """
    try:
        df = pd.read_csv(filepath)
        return df['Ticker'].tolist()
    except Exception as e:
        raise Exception(f"Error loading tickers: {str(e)}")

def save_results(results, output_path=None):
    """
    Save results to CSV file
    """
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f'data/output/financial_metrics_{timestamp}.csv'
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Define column order
    columns = [
        'ticker',
        'timestamp',
        'dividend_per_share',
        'current_price',
        'pb_ratio',
        'pe_ratio',
        'growth_rate',
        'target_yield_rate',
        'relative_pb',
        'peg_growth',
        'error'
    ]
    
    # Only include columns that exist
    existing_columns = [col for col in columns if col in df.columns]
    df = df[existing_columns]
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Ensure directories exist
    ensure_directory_exists('data/input')
    ensure_directory_exists('data/output')
    
    try:
        # Load tickers
        tickers = load_tickers(args.input)
        print(f"Loaded {len(tickers)} tickers")
        
        # Initialize scraper
        scraper = MorningstarScraper()
        results = []
        
        # Process each ticker
        for i, ticker in enumerate(tickers, 1):
            print(f"Processing {ticker} ({i}/{len(tickers)})")
            
            # Scrape data
            data = scraper.scrape_stock_data(ticker)
            results.append(data)
            
            # Save progress periodically
            if i % 10 == 0:
                save_results(results, args.output)
            
            # Delay between requests
            if i < len(tickers):  # Don't delay after last ticker
                time.sleep(args.delay)
        
        # Save final results
        save_results(results, args.output)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())