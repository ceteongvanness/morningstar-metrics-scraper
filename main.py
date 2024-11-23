import argparse
from src.scrapers.morningstar_scraper import MorningstarScraper
from src.formatters.csv_formatter import CSVFormatter
from src.utils.helpers import load_tickers, ensure_dir_exists
from src.utils.logger import setup_logger
from src.constants.config import INPUT_DIR, OUTPUT_DIR, LOGS_DIR

def parse_arguments():
    parser = argparse.ArgumentParser(description='Morningstar Stock Analysis Tool')
    parser.add_argument('--input', 
                      default=str(INPUT_DIR / 'tickers.csv'),
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
        ensure_dir_exists(INPUT_DIR)
        ensure_dir_exists(OUTPUT_DIR)
        ensure_dir_exists(LOGS_DIR)
        
        # Load tickers
        tickers = load_tickers(args.input)
        logger.info(f"Loaded {len(tickers)} tickers")
        
        # Initialize components
        scraper = MorningstarScraper()
        formatter = CSVFormatter()
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