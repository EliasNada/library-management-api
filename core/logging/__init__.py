import logging
import os
from logging.handlers import RotatingFileHandler

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=1024 * 1024 * 10, backupCount=5),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
