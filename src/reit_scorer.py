class REITScorer:
    def __init__(self):
        self.min_years = 10  # Analysis period in years

    def calculate_score(self, data):
        """
        Calculate total score based on REIT-specific criteria
        """
        try:
            scores = {}
            
            # EPS Stability Score
            scores['eps'] = {
                'score': self._score_eps_stability(data.get('eps_history', [])),
                'max_score': 1,
                'description': 'EPS 10年穩定'
            }
            
            # Dividend Score
            scores['dividend'] = {
                'score': self._score_dividend(data.get('dividend_history', [])),
                'max_score': 2,
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
                'description': '自由現金流10年正成長'
            }
            
            # FFO (Operating Cash Flow) Score
            scores['ffo'] = {
                'score': self._score_ffo(data.get('ffo_history', [])),
                'max_score': 1,
                'description': 'FFO 10年正成長'
            }
            
            # Net Margin Score
            scores['net_margin'] = {
                'score': self._score_net_margin(data.get('net_margin_history', [])),
                'max_score': 2,
                'description': '淨利率>10%且穩定'
            }
            
            # ROE Score
            scores['roe'] = {
                'score': self._score_roe_stability(data.get('roe_history', [])),
                'max_score': 1,
                'description': 'ROE 10年穩定'
            }
            
            # Interest Coverage Score
            scores['ic'] = {
                'score': self._score_interest_coverage(data.get('interest_coverage', 0)),
                'max_score': 2,
                'description': 'IC評分'
            }
            
            # Debt to Equity Score
            scores['debt_equity'] = {
                'score': self._score_debt_equity(data.get('debt_equity_ratio', 0)),
                'max_score': 1,
                'description': 'D/E < 0.5'
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

    def _score_eps_stability(self, eps_history):
        """Score EPS stability over 10 years"""
        if not eps_history or len(eps_history) < self.min_years:
            return 0
        
        # Calculate year-over-year changes
        changes = [abs((eps_history[i+1] - eps_history[i]) / eps_history[i]) 
                  for i in range(len(eps_history)-1)]
        
        # Consider stable if changes are within 20%
        is_stable = all(change <= 0.20 for change in changes)
        return 1 if is_stable else 0

    def _score_dividend(self, dividend_history):
        """Score dividend stability and growth"""
        if not dividend_history or len(dividend_history) < self.min_years:
            return 0
        
        score = 0
        
        # Check for consistent dividend payments
        if all(d > 0 for d in dividend_history):
            score += 1
        
        # Check for growing dividends
        if all(dividend_history[i] < dividend_history[i+1] for i in range(len(dividend_history)-1)):
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
        """Score free cash flow growth"""
        if not fcf_history or len(fcf_history) < self.min_years:
            return 0
        
        is_positive = all(fcf > 0 for fcf in fcf_history)
        is_growing = all(fcf_history[i] < fcf_history[i+1] for i in range(len(fcf_history)-1))
        
        return 1 if is_positive and is_growing else 0

    def _score_ffo(self, ffo_history):
        """Score FFO (Operating Cash Flow) growth"""
        if not ffo_history or len(ffo_history) < self.min_years:
            return 0
        
        is_positive = all(ffo > 0 for ffo in ffo_history)
        is_growing = all(ffo_history[i] < ffo_history[i+1] for i in range(len(ffo_history)-1))
        
        return 1 if is_positive and is_growing else 0

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

    def _score_roe_stability(self, roe_history):
        """Score ROE stability"""
        if not roe_history or len(roe_history) < self.min_years:
            return 0
        
        # Calculate year-over-year changes
        changes = [abs((roe_history[i+1] - roe_history[i]) / roe_history[i]) 
                  for i in range(len(roe_history)-1)]
        
        # Consider stable if changes are within 15%
        is_stable = all(change <= 0.15 for change in changes)
        return 1 if is_stable else 0

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

    def _score_debt_equity(self, de_ratio):
        """Score debt to equity ratio"""
        if not de_ratio:
            return 0
        return 1 if de_ratio < 0.5 else 0