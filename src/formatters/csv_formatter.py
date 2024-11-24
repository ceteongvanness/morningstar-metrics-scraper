import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from ..utils.logger import setup_logger
from ..utils.helpers import format_output_path, get_timestamp_filename
from ..constants.config import COLUMNS, CSV_ENCODING

class CSVFormatter:
    def __init__(self):
        self.logger = setup_logger('csv_formatter')
        self.columns = list(COLUMNS.values())

    def read_input_csv(self, input_path: str) -> List[str]:
        """Read tickers from input CSV file"""
        try:
            df = pd.read_csv(input_path, encoding=CSV_ENCODING)
            # Debug print
            print("Available columns in CSV:", df.columns.tolist())
            
            # Get the ticker column name from COLUMNS config
            ticker_column = COLUMNS.get('TICKER')
            print("Looking for column:", ticker_column)
            
            if ticker_column not in df.columns:
                self.logger.error(f"Column {ticker_column} not found in CSV")
                return []
            
            # Get unique tickers and remove any empty/null values
            tickers = df[ticker_column].dropna().unique().tolist()
            self.logger.info(f"Found {len(tickers)} unique tickers in {input_path}")
            return tickers
            
        except Exception as e:
            self.logger.error(f"Error reading input CSV: {str(e)}")
            return []

    def format_data(self, data_list: List[Dict[str, Any]]) -> pd.DataFrame:
        """Format scraped data into DataFrame"""
        formatted_data = []
        
        for data in data_list:
            row = {
                COLUMNS['TICKER']: str(data.get('ticker', '')),
                COLUMNS['SECTOR']: str(data.get('sector', '')),
                COLUMNS['INDUSTRY']: str(data.get('industry', '')),
                COLUMNS['CURRENT_PRICE']: self._format_number(data.get('current_price', 0)),
                COLUMNS['TARGET_YIELD']: self._calculate_target_yield(
                    data.get('dividend_ttm', 0),
                    data.get('yield_5yr_avg', 0)
                ),
                COLUMNS['PB_RATIO']: self._calculate_pb_valuation(
                    data.get('bvps_ttm', 0),
                    data.get('pb_5yr_avg', 0)
                ),
                COLUMNS['PEG_RATIO']: self._calculate_peg_valuation(
                    data.get('eps_ttm', 0),
                    data.get('eps_growth', 0)
                ),
                COLUMNS['DIVIDEND_TTM']: self._format_number(data.get('dividend_ttm', 0)),
                COLUMNS['YIELD_5YR_AVG']: self._format_percentage(data.get('yield_5yr_avg', 0)),
                COLUMNS['BVPS_TTM']: self._format_number(data.get('bvps_ttm', 0)),
                COLUMNS['PB_5YR_AVG']: self._format_number(data.get('pb_5yr_avg', 0)),
                COLUMNS['EPS_TTM']: self._format_number(data.get('eps_ttm', 0)),
                COLUMNS['EPS_GROWTH']: self._format_percentage(data.get('eps_growth', 0))
            }
            formatted_data.append(row)
        
        return pd.DataFrame(formatted_data, columns=self.columns)

    def save_to_csv(self, df: pd.DataFrame, output_path: str = None) -> None:
        """Save DataFrame to CSV with timestamp"""
        try:
            if output_path is None:
                output_path = format_output_path()
            else:
                directory = os.path.dirname(output_path)
                filename = os.path.basename(output_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(directory, get_timestamp_filename(name))
            
            # Save with UTF-8-BOM encoding for proper Chinese character display
            df.to_csv(output_path, index=False, encoding=CSV_ENCODING)
            self.logger.info(f"Data saved to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {str(e)}")

    def _calculate_target_yield(self, dividend_ttm: float, yield_5yr_avg: float) -> str:
        """Calculate target yield valuation"""
        try:
            if yield_5yr_avg and yield_5yr_avg != 0:
                return self._format_number(dividend_ttm / (yield_5yr_avg * 1.2))
            return "0.00"
        except:
            return "0.00"

    def _calculate_pb_valuation(self, bvps_ttm: float, pb_5yr_avg: float) -> str:
        """Calculate P/B valuation"""
        try:
            return self._format_number(bvps_ttm * pb_5yr_avg)
        except:
            return "0.00"

    def _calculate_peg_valuation(self, eps_ttm: float, eps_growth: float) -> str:
        """Calculate PEG valuation"""
        try:
            return self._format_number(eps_ttm * eps_growth * 100)
        except:
            return "0.00"

    def _format_number(self, value: float) -> str:
        """Format numeric values"""
        try:
            return f"{float(value):,.2f}"
        except:
            return "0.00"

    def _format_percentage(self, value: float) -> str:
        """Format percentage values"""
        try:
            return f"{float(value):,.2f}"
        except:
            return "0.00"