import logging
from datetime import datetime
from pathlib import Path
from ..constants.config import LOGS_DIR, LOG_FORMAT, LOG_LEVEL

def setup_logger(name: str = 'morningstar_scraper') -> logging.Logger:
    """Configure and return a logger instance"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)
    
    # Create formatters and handlers
    formatter = logging.Formatter(LOG_FORMAT)
    
    # File handler
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_handler = logging.FileHandler(
        filename=Path(LOGS_DIR) / f'scraper_{timestamp}.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger