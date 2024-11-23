from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
INPUT_DIR = DATA_DIR / 'input'
OUTPUT_DIR = DATA_DIR / 'output'
LOGS_DIR = PROJECT_ROOT / 'logs'

# Scraping settings
MORNINGSTAR_URL = "https://www.morningstar.com"
FINVIZ_URL = "https://finviz.com"
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 2
MAX_RETRIES = 3

# Output settings
CSV_ENCODING = 'utf-8-sig'
DATE_FORMAT = '%Y%m%d_%H%M%S'

# Headers for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Column names
# Updated column names to include Finviz data
COLUMNS = {
    'TICKER': '股票代碼',
    'SECTOR': '產業類別',
    'INDUSTRY': '產業',
    'CURRENT_PRICE': '現在股價',
    'TARGET_YIELD': '目標殖利率 估價法',
    'PB_RATIO': '相對 P/B 估價法',
    'PEG_RATIO': 'PEG 成長股 估價法',
    'DIVIDEND_TTM': '該公司 股息(TTM)',
    'YIELD_5YR_AVG': '該公司近5年 平均殖利率',
    'BVPS_TTM': '該公司 BVPS(TTM)',
    'PB_5YR_AVG': '該公司近5年 平均P/B',
    'EPS_TTM': '該公司 EPS(TTM)',
    'EPS_GROWTH': '該公司 EPS成長率％',
    'FINVIZ_PE': 'Finviz P/E',
    'FINVIZ_FWD_PE': 'Finviz Forward P/E',
    'FINVIZ_PEG': 'Finviz PEG',
    'FINVIZ_PB': 'Finviz P/B',
    'FINVIZ_DIV': 'Finviz Dividend %',
    'FINVIZ_ROE': 'Finviz ROE',
    'FINVIZ_ROA': 'Finviz ROA',
    'FINVIZ_EPS': 'Finviz EPS',
    'FINVIZ_BETA': 'Finviz Beta'
}