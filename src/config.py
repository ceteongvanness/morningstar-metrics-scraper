import os
from dotenv import load_dotenv

# Load environment variables, but don't fail if .env doesn't exist
load_dotenv(override=True)

# Base configuration
BASE_URL = os.getenv('BASE_URL', "https://www.morningstar.com/stocks")
DEFAULT_DELAY = int(os.getenv('DEFAULT_DELAY', 2))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))

# Request headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

# File paths
INPUT_DIR = 'data/input'
OUTPUT_DIR = 'data/output'
DEFAULT_INPUT_FILE = os.path.join(INPUT_DIR, 'tickers.csv')

# Logging configuration
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')