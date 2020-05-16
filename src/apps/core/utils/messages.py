"""Module for messages"""
from django.conf import settings

MESSAGES = {
    'REGISTER': 'successfully registered.',
    'LOGIN': 'successfully logged in.'
}

ERRORS = {
    'USR_01': 'Enter a valid email address.',
    'USR_02': 'Password must be alphanumeric and must contain at least '
    'one special character.',
    'USR_O3': 'There is a problem with the values provided.',
    'USR_04': 'We could not find what you\'re looking for.',
    'USR_05': 'Invalid Id provided.',
    'FILE_01': 'Image file too large, must not be above '
    f'{int(str(settings.MAX_IMAGE_SIZE)[:1])} Megabyte.',
    'FILE_02': 'There is an error with the image file.',
    'FILE_03': 'Could not find any Image file.',
    'FILE_04': 'Image cannot be opened or identified.',
}
