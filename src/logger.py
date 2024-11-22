import logging
from .config import LOG_FORMAT, LOG_LEVEL

def setup_logger(name='morningstar_scraper'):
    """Configure and return a logger instance"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    return logger