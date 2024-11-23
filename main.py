import argparse
from src.scrapers.combined_scraper import CombinedScraper
from src.formatters.csv_formatter import CSVFormatter
from src.utils.helpers import load_tickers, setup_project_structure
from src.utils.logger import setup_logger
from src.constants.config import INPUT_DIR
from pathlib import Path

def main():
    logger = setup_logger('main')
    args = parse_arguments()
    
    try:
        setup_project_structure()
        
        # Load tickers
        tickers = load_tickers(args.input)
        logger.info(f"Loaded {len(tickers)} tickers")
        
        # Initialize components
        scraper = CombinedScraper()
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