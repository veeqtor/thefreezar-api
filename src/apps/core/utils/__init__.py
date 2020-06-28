"""Init"""
import logging
from dateutil import parser
from datetime import datetime

# Get the logger specified in the file
from src.apps.core.utils.response import ResponseHandler

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def date_validator(date_value):
    """Validates date format

     Arguments:
        date_value (string): date string

     Raises:
        ValidationError: Used to raise exception if date format is not valid

    Returns:
        date: the validated date
    """
    try:
        parser.parse(date_value).date()
        date = datetime.strptime(date_value, '%Y-%m-%d')
        return date
    except ValueError as e:
        logger.error(e)
        ResponseHandler.raise_error(dict(date=e))
