class NormalStockScorer:
    def __init__(self):
        self.min_years = 10  # Analysis period in years

    def calculate_score(self, data):
        """
        Calculate total score based on both financial metrics and competitive advantages
        """
        try:
            # Financial Metrics Scoring
            financial_scores = {
                'eps': {
                    'score': self._score_eps_growth(data.get('eps_history', [])),
                    'max_score': 1,
                    'description': 'EPS 10年穩定成長'
                },
                'dividend': {
                    'score': self._score_dividend(data.get('dividend_history', [])),
                    'max_score': 1.5,  # 0.5 for stability + 1 for growth
                    'description': '股息穩定性(0.5)和成長(1)'
                },
                'shares': {
                    'score': self._score_shares(data.get('shares_history', [])),
                    'max_score': 1,
                    'description': '流通股數10年穩定減少'
                },
                'book_value': {
                    'score': self._score_book_value(data.get('bvps_history', [])),
                    'max_score': 1,
                    'description': '每股淨值10年穩定成長'
                },
                'fcf': {
                    'score': self._score_fcf(data.get('fcf_history', [])),
                    'max_score': 1,
                    'description': '自由現金流10年皆為正數'
                },
                'net_margin': {
                    'score': self._score_net_margin(data.get('net_margin_history', [])),
                    'max_score': 1.5,  # 1 for >10% + 0.5 for stability
                    'description': '淨利率>10%(1)且穩定(0.5)'
                },
                'roe': {
                    'score': self._score_roe(data.get('roe_history', [])),
                    'max_score': 1,
                    'description': 'ROE 評分'
                },
                'ic': {
                    'score': self._score_interest_coverage(data.get('interest_coverage', 0)),
                    'max_score': 1.5,  # 1 for >10 + 0.5 for >5
                    'description': 'IC評分'
                },
                'debt_equity': {
                    'score': self._score_debt_equity(data.get('debt_equity_ratio', 0)),
                    'max_score': 1,
                    'description': 'D/E < 0.5'
                }
            }

            # Competitive Advantage Scoring
            moat_scores = {
                'brand': {
                    'score': self._score_brand(data.get('brand_metrics', {})),
                    'max_score': 1,
                    'description': '品牌優勢'
                },
                'patent': {
                    'score': self._score_patent(data.get('patent_metrics', {})),
                    'max_score': 1,
                    'description': '專利、特許執照'
                },
                'cost_advantage': {
                    'score': self._score_cost_advantage(data.get('cost_metrics', {})),
                    'max_score': 1,
                    'description': '成本優勢'
                },
                'switching_cost': {
                    'score': self._score_switching_cost(data.get('switching_metrics', {})),
                    'max_score': 1,
                    'description': '高轉換成本'
                },
                'network_effect': {
                    'score': self._score_network_effect(data.get('network_metrics', {})),
                    'max_score': 1,
                    'description': '網絡效應'
                },
                'niche_market': {
                    'score': self._score_niche_market(data.get('market_metrics', {})),
                    'max_score': 1,
                    'description': '利基市場'
                },
                'confidence': {
                    'score': self._score_confidence(data.get('confidence_metrics', {})),
                    'max_score': 1,
                    'description': '長期存在信心'
                }
            }

            # Risk Assessment
            risk_scores = self._calculate_risk_deductions(data)

            # Calculate total scores
            financial_total = sum(item['score'] for item in financial_scores.values())
            moat_total = sum(item['score'] for item in moat_scores.values())
            risk_total = sum(risk_scores.values())

            return {
                'financial_scores': financial_scores,
                'moat_scores': moat_scores,
                'risk_scores': risk_scores,
                'financial_total': financial_total,
                'moat_total': moat_total,
                'risk_total': risk_total,
                'final_score': financial_total + moat_total + risk_total
            }

        except Exception as e:
            return {'error': str(e)}

    def _score_eps_growth(self, eps_history):
        """Score EPS growth over 10 years"""
        if not eps_history or len(eps_history) < self.min_years:
            return 0
        return 1 if all(eps_history[i] < eps_history[i+1] for i in range(len(eps_history)-1)) else 0

    def _score_dividend(self, dividend_history):
        """Score dividend stability and growth"""
        if not dividend_history or len(dividend_history) < self.min_years:
            return 0
        
        score = 0
        # Stable dividend
        if all(d > 0 for d in dividend_history):
            score += 0.5
        # Growing dividend
        if all(dividend_history[i] < dividend_history[i+1] for i in range(len(dividend_history)-1)):
            score += 1
        return score

    def _score_net_margin(self, margin_history):
        """Score net margin"""
        if not margin_history or len(margin_history) < self.min_years:
            return 0
        
        score = 0
        # Above 10%
        if all(margin > 10 for margin in margin_history):
            score += 1
        # Stability
        if all(margin_history[i] <= margin_history[i+1] for i in range(len(margin_history)-1)):
            score += 0.5
        return score

    def _score_roe(self, roe_history):
        """Score ROE"""
        if not roe_history or len(roe_history) < self.min_years:
            return 0
        
        # Check if ROE is between 15% and 40%
        if all(15 < roe < 40 for roe in roe_history):
            return 1
        # Check if ROE is below 15% but growing
        if all(roe < 15 for roe in roe_history) and \
           all(roe_history[i] < roe_history[i+1] for i in range(len(roe_history)-1)):
            return 0.5
        return 0

    def _calculate_risk_deductions(self, data):
        """Calculate risk deductions"""
        risk_scores = {
            'tech_risk': 0,
            'govt_risk': 0,
            'china_risk': 0
        }
        
        if data.get('is_tech_company', False) or data.get('is_fashion_company', False):
            risk_scores['tech_risk'] = -1
        
        if data.get('is_policy_sensitive', False):
            risk_scores['govt_risk'] = -1
        
        if data.get('is_chinese_adr', False):
            risk_scores['china_risk'] = -1
        
        return risk_scores

    # ... [Additional scoring methods for competitive advantages] ...