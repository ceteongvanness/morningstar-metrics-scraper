import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from ..utils.logger import setup_logger

class OutputFormatter:
    def __init__(self):
        self.logger = setup_logger('output_formatter')
        self.columns = [
            '股票代碼',
            '現在股價',
            '目標殖利率 估價法',
            '相對 P/B 估價法',
            'PEG 成長股 估價法',
            '該公司 股息(TTM)',
            '該公司近5年 平均殖利率',
            '該公司 BVPS(TTM)',
            '該公司近5年 平均P/B',
            '該公司 EPS(TTM)',
            '該公司 EPS成長率％'
        ]

    def format_data(self, data_list: List[Dict[str, Any]]) -> pd.DataFrame:
        """Format scraped data into DataFrame"""
        formatted_data = []
        
        for data in data_list:
            row = {
                '股票代碼': data.get('ticker', ''),
                '現在股價': self._format_number(data.get('current_price', 0)),
                '目標殖利率 估價法': self._calculate_target_yield(
                    data.get('dividend_ttm', 0),
                    data.get('yield_5yr_avg', 0)
                ),
                '相對 P/B 估價法': self._calculate_pb_valuation(
                    data.get('bvps_ttm', 0),
                    data.get('pb_5yr_avg', 0)
                ),
                'PEG 成長股 估價法': self._calculate_peg_valuation(
                    data.get('eps_ttm', 0),
                    data.get('eps_growth', 0)
                ),
                '該公司 股息(TTM)': self._format_number(data.get('dividend_ttm', 0)),
                '該公司近5年 平均殖利率': self._format_percentage(data.get('yield_5yr_avg', 0)),
                '該公司 BVPS(TTM)': self._format_number(data.get('bvps_ttm', 0)),
                '該公司近5年 平均P/B': self._format_number(data.get('pb_5yr_avg', 0)),
                '該公司 EPS(TTM)': self._format_number(data.get('eps_ttm', 0)),
                '該公司 EPS成長率％': self._format_percentage(data.get('eps_growth', 0))
            }
            formatted_data.append(row)
        
        return pd.DataFrame(formatted_data, columns=self.columns)

    def save_to_csv(self, df: pd.DataFrame, output_path: str = None) -> None:
        """Save DataFrame to CSV with timestamp"""
        try:
            if output_path is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = f'data/output/stock_analysis_{timestamp}.csv'
            
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
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