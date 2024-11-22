import os
import logging

def ensure_directory_exists(path):
    """
    Create directory if it doesn't exist
    """
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")

def validate_csv_file(filepath):
    """
    Validate CSV file exists and has required columns
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)
    if 'Ticker' not in df.columns:
        raise ValueError("CSV file must contain a 'Ticker' column")