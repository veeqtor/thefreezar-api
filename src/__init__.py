"""Init"""

# This will make sure the celery app is imported once django starts
from src.celery import app as celery_app

__all__ = ['celery_app']
