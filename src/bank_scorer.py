class BankStockScorer:
    def __init__(self):
        self.min_years = 10  # Analysis period in years

    def calculate_score(self, data):
        """
        Calculate total score based on banking-specific criteria
        """
        try:
            scores = {}
            
            # EPS Growth Score
            scores['eps'] = {
                'score': self._score_eps_growth(data.get('eps_history', [])),
                'max_score': 1,
                'description': 'EPS 10年穩定成長'
            }
            
            # Dividend Score
            dividend_score = self._score_dividend(
                data.get('dividend_history', []),
                data.get('dividend_growth_5y', 0),
                data.get('dividend_growth_10y', 0)
            )
            scores['dividend'] = {
                'score': dividend_score,
                'max_score': 3,
                'description': '股息穩定性和成長性'
            }
            
            # Shares Outstanding Score
            scores['shares'] = {
                'score': self._score_shares(data.get('shares_history', [])),
                'max_score': 1,
                'description': '流通股數10年穩定減少'
            }
            
            # Book Value Per Share Score
            scores['bvps'] = {
                'score': self._score_bvps(data.get('bvps_history', [])),
                'max_score': 1,
                'description': '每股淨資產10年穩定成長'
            }
            
            # FCF Score
            scores['fcf'] = {
                'score': self._score_fcf(data.get('fcf_history', [])),
                'max_score': 1,
                'description': '自由現金流10年皆為正數'
            }
            
            # Net Margin Score
            scores['net_margin'] = {
                'score': self._score_net_margin(data.get('net_margin_history', [])),
                'max_score': 2,
                'description': '淨利率>10%且穩定'
            }
            
            # ROA Score
            scores['roa'] = {
                'score': self._score_roa(data.get('roa_history', [])),
                'max_score': 1,
                'description': 'ROA > 1.2% for 10 years'
            }
            
            # Interest Coverage Score
            scores['ic'] = {
                'score': self._score_interest_coverage(data.get('interest_coverage', 0)),
                'max_score': 2,
                'description': 'IC評分'
            }
            
            # Interest Income Ratio Score
            scores['interest_income_ratio'] = {
                'score': self._score_interest_income_ratio(data.get('interest_income_ratio', 0)),
                'max_score': 1,
                'description': '利息收入比>50%'
            }

            # Calculate total score
            total_score = sum(item['score'] for item in scores.values())
            max_possible = sum(item['max_score'] for item in scores.values())

            return {
                'total_score': total_score,
                'max_possible': max_possible,
                'detailed_scores': scores,
                'score_percentage': (total_score / max_possible) * 100 if max_possible > 0 else 0
            }

        except Exception as e:
            return {
                'error': str(e),
                'total_score': 0,
                'detailed_scores': {},
                'score_percentage': 0
            }

    def _score_eps_growth(self, eps_history):
        """Score EPS growth over 10 years"""
        if not eps_history or len(eps_history) < self.min_years:
            return 0
        
        is_growing = all(eps_history[i] < eps_history[i+1] for i in range(len(eps_history)-1))
        return 1 if is_growing else 0

    def _score_dividend(self, dividend_history, growth_5y, growth_10y):
        """Score dividend based on multiple criteria"""
        if not dividend_history or len(dividend_history) < self.min_years:
            return 0
        
        score = 0
        
        # Check for consistent dividend payments
        if all(d > 0 for d in dividend_history):
            score += 1
            
        # Check for growing dividends
        if all(dividend_history[i] < dividend_history[i+1] for i in range(len(dividend_history)-1)):
            score += 1
            
        # Compare 5-year vs 10-year growth rates
        if growth_5y and growth_10y and growth_5y > growth_10y:
            score += 1
            
        return score

    def _score_shares(self, shares_history):
        """Score shares outstanding trend"""
        if not shares_history or len(shares_history) < self.min_years:
            return 0
        
        is_decreasing = all(shares_history[i] > shares_history[i+1] for i in range(len(shares_history)-1))
        return 1 if is_decreasing else 0

    def _score_bvps(self, bvps_history):
        """Score book value per share growth"""
        if not bvps_history or len(bvps_history) < self.min_years:
            return 0
        
        is_growing = all(bvps_history[i] < bvps_history[i+1] for i in range(len(bvps_history)-1))
        return 1 if is_growing else 0

    def _score_fcf(self, fcf_history):
        """Score free cash flow"""
        if not fcf_history or len(fcf_history) < self.min_years:
            return 0
        
        all_positive = all(fcf > 0 for fcf in fcf_history)
        return 1 if all_positive else 0

    def _score_net_margin(self, margin_history):
        """Score net margin based on threshold and stability"""
        if not margin_history or len(margin_history) < self.min_years:
            return 0
        
        score = 0
        
        # Check if all margins are above 10%
        if all(margin > 10 for margin in margin_history):
            score += 1
            
        # Check for stability/growth
        if all(margin_history[i] <= margin_history[i+1] for i in range(len(margin_history)-1)):
            score += 1
            
        return score

    def _score_roa(self, roa_history):
        """Score ROA based on threshold"""
        if not roa_history or len(roa_history) < self.min_years:
            return 0
        
        all_above_threshold = all(roa > 1.2 for roa in roa_history)
        return 1 if all_above_threshold else 0

    def _score_interest_coverage(self, ic):
        """Score interest coverage ratio"""
        if not ic or ic == "-":
            return 2  # Maximum score for no debt
        
        score = 0
        if ic > 10:
            score += 1
        if ic > 5:
            score += 1
        return score

    def _score_interest_income_ratio(self, ratio):
        """Score interest income ratio"""
        if not ratio:
            return 0
        
        return 1 if ratio > 50 else 0