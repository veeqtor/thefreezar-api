"""Init"""
import logging

# Get the logger specified in the file
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
