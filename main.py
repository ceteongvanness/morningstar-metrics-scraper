import argparse
from src.scraper.morningstar_scraper import MorningstarScraper
from src.output.formatter import OutputFormatter
from src.utils.helpers import load_tickers, ensure_dir_exists
from src.utils.logger import setup_logger

def parse_arguments():
    parser = argparse.ArgumentParser(description='Morningstar Stock Analysis Tool')
    parser.add_argument('--input', 
                      default='data/input/tickers.csv',
                      help='Path to input CSV file with tickers')
    parser.add_argument('--output',
                      help='Path to output CSV file (optional)')
    return parser.parse_args()

def main():
    # Set up logging
    logger = setup_logger('main')
    
    # Parse arguments
    args = parse_arguments()
    
    try:
        # Ensure directories exist
        ensure_dir_exists('data/input')
        ensure_dir_exists('data/output')
        ensure_dir_exists('logs')
        
        # Load tickers
        tickers = load_tickers(args.input)
        logger.info(f"Loaded {len(tickers)} tickers")
        
        # Initialize components
        scraper = MorningstarScraper()
        formatter = OutputFormatter()
        results = []
        
        # Process each ticker
        for i, ticker in enumerate(tickers, 1):
            logger.info(f"Processing {ticker} ({i}/{len(tickers)})")
            data = scraper.scrape_stock_data(ticker)
            results.append(data)
        
        # Format and save results
        df = formatter.format_data(results)
        formatter.save_to_csv(df, args.output)
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())