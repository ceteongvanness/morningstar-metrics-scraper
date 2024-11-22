import pandas as pd
from datetime import datetime

class StockAnalysisOutput:
    def __init__(self):
        self.columns = {
            'stock_code': '股票代碼',
            'current_price': '現在股價',
            'total_score': '總評分',
            'financial_score': '財報評分',
            'moat_score': '護城河評分',
            'risk_deduction': '風險扣分',
            'target_yield_price': '目標殖利率 估價法',
            'relative_pb_price': '相對 P/B 估價法',
            'peg_price': 'PEG 成長股 估價法',
            'dividend_ttm': '該公司 股息(TTM)',
            'yield_5yr_avg': '該公司近5年 平均殖利率',
            'bvps_ttm': '該公司 BVPS(TTM)',
            'pb_5yr_avg': '該公司近5年 平均P/B',
            'eps_ttm': '該公司 EPS(TTM)',
            'eps_growth': '該公司 EPS成長率％'
        }

    def generate_output(self, stock_data, score_results):
        """
        Generate formatted output DataFrame
        """
        try:
            data = {
                self.columns['stock_code']: [stock_data.get('stock_code', '')],
                self.columns['current_price']: [stock_data.get('current_price', 0)],
                self.columns['total_score']: [score_results.get('final_score', 0)],
                self.columns['financial_score']: [score_results.get('financial_total', 0)],
                self.columns['moat_score']: [score_results.get('moat_total', 0)],
                self.columns['risk_deduction']: [score_results.get('risk_total', 0)],
                
                # Valuation metrics
                self.columns['target_yield_price']: [self._calculate_target_yield_price(stock_data)],
                self.columns['relative_pb_price']: [self._calculate_relative_pb_price(stock_data)],
                self.columns['peg_price']: [self._calculate_peg_price(stock_data)],
                
                # Raw metrics
                self.columns['dividend_ttm']: [stock_data.get('dividend_ttm', 0)],
                self.columns['yield_5yr_avg']: [stock_data.get('yield_5yr_avg', 0)],
                self.columns['bvps_ttm']: [stock_data.get('bvps_ttm', 0)],
                self.columns['pb_5yr_avg']: [stock_data.get('pb_5yr_avg', 0)],
                self.columns['eps_ttm']: [stock_data.get('eps_ttm', 0)],
                self.columns['eps_growth']: [stock_data.get('eps_growth', 0)]
            }
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Error generating output: {str(e)}")
            return pd.DataFrame()

    def save_to_csv(self, df, filename=None):
        """
        Save the analysis to CSV file
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'stock_analysis_{timestamp}.csv'
            
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Analysis saved to {filename}")
            
        except Exception as e:
            print(f"Error saving to CSV: {str(e)}")

    def _calculate_target_yield_price(self, data):
        """Calculate target price based on yield method"""
        try:
            dividend_ttm = data.get('dividend_ttm', 0)
            yield_5yr_avg = data.get('yield_5yr_avg', 0)
            if dividend_ttm and yield_5yr_avg:
                return dividend_ttm / (yield_5yr_avg * 1.2)
            return 0
        except:
            return 0

    def _calculate_relative_pb_price(self, data):
        """Calculate target price based on P/B method"""
        try:
            bvps_ttm = data.get('bvps_ttm', 0)
            pb_5yr_avg = data.get('pb_5yr_avg', 0)
            if bvps_ttm and pb_5yr_avg:
                return bvps_ttm * pb_5yr_avg
            return 0
        except:
            return 0

    def _calculate_peg_price(self, data):
        """Calculate target price based on PEG method"""
        try:
            eps_ttm = data.get('eps_ttm', 0)
            eps_growth = data.get('eps_growth', 0)
            if eps_ttm and eps_growth:
                return eps_ttm * eps_growth * 100
            return 0
        except:
            return 0