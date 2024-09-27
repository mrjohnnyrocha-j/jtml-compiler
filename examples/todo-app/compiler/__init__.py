import logging

logging.basicConfig(
    level=logging.INFO,  # Set default logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('compiler.log'),  # Log to file
    ]
)

logger = logging.getLogger(__name__)
