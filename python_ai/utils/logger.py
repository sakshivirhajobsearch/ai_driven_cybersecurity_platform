# python_ai/utils/logger.py

import logging
import os
from datetime import datetime

# ===============================
# CONFIGURATION
# ===============================
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file name with timestamp
log_filename = os.path.join(LOG_DIR, f"cybersec_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# ===============================
# LOGGER SETUP
# ===============================
def get_logger(name: str):
    """
    Returns a configured logger instance.
    
    Args:
        name (str): Name of the logger (usually __name__)
    
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid adding multiple handlers to the same logger
    if not logger.handlers:

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
