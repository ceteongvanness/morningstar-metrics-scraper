# Morningstar page selectors
SELECTORS = {
    'quote': {
        'current_price': 'div[data-test="current-price"]',
        'price_value': 'span[data-test="price-value"]'
    },
    'dividends': {
        'dividend_ttm': 'div[data-test="dividend-ttm"]',
        'yield_5yr_avg': 'div[data-test="yield-5yr-avg"]'
    },
    'valuation': {
        'bvps_ttm': 'div[data-test="bvps-ttm"]',
        'pb_5yr_avg': 'div[data-test="pb-5yr-avg"]'
    },
    'financials': {
        'eps_ttm': 'div[data-test="eps-ttm"]',
        'eps_growth': 'div[data-test="eps-growth"]'
    }
}

# Page URLs
PAGE_URLS = {
    'quote': '/quote',
    'dividends': '/dividends',
    'valuation': '/valuation',
    'financials': '/financials'
}