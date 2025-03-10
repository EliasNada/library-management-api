import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=1024 * 1024 * 10, backupCount=5),  # 10 MB per file, 5 backups
        logging.StreamHandler(),  # Log to console
    ],
)

logger = logging.getLogger(__name__)
