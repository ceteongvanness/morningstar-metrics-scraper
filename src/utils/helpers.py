import os
import pandas as pd
from pathlib import Path
from typing import List, Any, Union
from datetime import datetime
from ..constants.config import INPUT_DIR, OUTPUT_DIR, LOGS_DIR, DATE_FORMAT

def ensure_dir_exists(path: Union[str, Path]) -> None:
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def load_tickers(filepath: Union[str, Path]) -> List[str]:
    """Load tickers from CSV file"""
    try:
        ensure_dir_exists(INPUT_DIR)
        df = pd.read_csv(filepath)
        return df['Ticker'].tolist()
    except Exception as e:
        raise Exception(f"Error loading tickers: {str(e)}")

def clean_numeric(value: Any) -> float:
    """Clean and convert numeric string to float"""
    try:
        if value is None:
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        cleaned = str(value).replace('$', '').replace(',', '').replace('%', '')
        return float(cleaned)
    except (ValueError, AttributeError):
        return 0.0

def get_timestamp_filename(base_name: str = 'result') -> str:
    """Generate filename with timestamp"""
    timestamp = datetime.now().strftime(DATE_FORMAT)
    return f"{base_name}_{timestamp}.csv"

def format_output_path(filename: str = None) -> Path:
    """Format output file path with timestamp"""
    ensure_dir_exists(OUTPUT_DIR)
    if filename is None:
        filename = get_timestamp_filename()
    return OUTPUT_DIR / filename

def setup_project_structure() -> None:
    """Create all necessary project directories"""
    for directory in [INPUT_DIR, OUTPUT_DIR, LOGS_DIR]:
        ensure_dir_exists(directory)