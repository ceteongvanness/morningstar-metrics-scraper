import pandas as pd
from datetime import datetime
import os

class OutputFormatter:
    def __init__(self):
        self.columns = [
            '股票代碼',               # Stock code
            '現在股價',               # Current price
            '目標殖利率 估價法',        # Target yield valuation
            '相對 P/B 估價法',         # Relative P/B valuation
            'PEG 成長股 估價法',       # PEG growth valuation
            '該公司 股息(TTM)',        # Company dividend TTM
            '該公司近5年 平均殖利率',    # 5-year average yield
            '該公司 BVPS(TTM)',       # Company BVPS TTM
            '該公司近5年 平均P/B',      # 5-year average P/B
            '該公司 EPS(TTM)',        # Company EPS TTM
            '該公司 EPS成長率％'        # Company EPS growth rate
        ]

    def format_output(self, data_list):
        """
        Format the scraped data into a DataFrame with required columns
        """
        formatted_data = []
        
        for data in data_list:
            # Calculate valuations
            target_yield = self._calculate_target_yield(
                data.get('dividend_ttm', 0),
                data.get('yield_5yr_avg', 0)
            )
            
            relative_pb = self._calculate_relative_pb(
                data.get('bvps_ttm', 0),
                data.get('pb_5yr_avg', 0)
            )
            
            peg_valuation = self._calculate_peg(
                data.get('eps_ttm', 0),
                data.get('eps_growth', 0)
            )
            
            # Format row data
            row = {
                '股票代碼': str(data.get('ticker', '')),
                '現在股價': self._format_number(data.get('current_price', 0)),
                '目標殖利率 估價法': self._format_number(target_yield),
                '相對 P/B 估價法': self._format_number(relative_pb),
                'PEG 成長股 估價法': self._format_number(peg_valuation),
                '該公司 股息(TTM)': self._format_number(data.get('dividend_ttm', 0)),
                '該公司近5年 平均殖利率': self._format_percentage(data.get('yield_5yr_avg', 0)),
                '該公司 BVPS(TTM)': self._format_number(data.get('bvps_ttm', 0)),
                '該公司近5年 平均P/B': self._format_number(data.get('pb_5yr_avg', 0)),
                '該公司 EPS(TTM)': self._format_number(data.get('eps_ttm', 0)),
                '該公司 EPS成長率％': self._format_percentage(data.get('eps_growth', 0))
            }
            formatted_data.append(row)
        
        # Create DataFrame with specified column order
        df = pd.DataFrame(formatted_data, columns=self.columns)
        return df

    def save_to_csv(self, df, output_path=None):
        """
        Save the formatted DataFrame to CSV with datetime in filename
        """
        try:
            # Get current datetime for filename
            current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Create output directory if it doesn't exist
            os.makedirs('data/output', exist_ok=True)
            
            if output_path is None:
                # Default filename with datetime
                output_path = f'data/output/result_{current_datetime}.csv'
            else:
                # Add datetime to custom filename
                directory = os.path.dirname(output_path)
                filename = os.path.basename(output_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(directory, f'{name}_{current_datetime}{ext}')
            
            # Save with UTF-8-BOM encoding for proper Chinese character display
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"Analysis saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving to CSV: {str(e)}")
            return False

    def _calculate_target_yield(self, dividend_ttm, yield_5yr_avg):
        """Calculate target yield valuation"""
        try:
            if yield_5yr_avg and yield_5yr_avg != 0:
                return dividend_ttm / (yield_5yr_avg * 1.2)
            return 0
        except:
            return 0

    def _calculate_relative_pb(self, bvps_ttm, pb_5yr_avg):
        """Calculate relative P/B valuation"""
        try:
            return bvps_ttm * pb_5yr_avg
        except:
            return 0

    def _calculate_peg(self, eps_ttm, eps_growth):
        """Calculate PEG valuation"""
        try:
            return eps_ttm * eps_growth * 100
        except:
            return 0

    def _format_number(self, value):
        """Format numeric values"""
        try:
            return f"{float(value):,.2f}"
        except:
            return "0.00"

    def _format_percentage(self, value):
        """Format percentage values"""
        try:
            return f"{float(value):,.2f}"
        except:
            return "0.00"