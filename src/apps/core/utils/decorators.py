"""Decorators"""
from functools import wraps
import uuid

from src.apps.core.utils.messages import ERRORS
from src.apps.core.utils.response import ResponseHandler


def validate_id(func):
    """
    Decorator function to validate UUID
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """
        Decorated function.
        """
        request, = args
        pk = request.kwargs.get('pk', None)
        if pk:
            try:
                uuid.UUID(pk, version=4)
            except ValueError:
                return ResponseHandler.raise_error(ERRORS['USR_05'])
        return func(*args, **kwargs)

    return decorated_function
