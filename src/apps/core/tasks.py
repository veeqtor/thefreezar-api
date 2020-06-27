"""Shared celery tasks"""
from datetime import datetime

from django.conf import settings
import cloudinary.uploader
from celery import shared_task
from src.apps.core.utils import logger
from src.apps.core.utils.response import ResponseHandler


@shared_task(name='upload-image')
def upload_image(file_path, is_async=True, **kwargs):
    """Method to upload image file to cloudinary."""
    eager = {
        'width': kwargs.get('width', 1024),
        'height': kwargs.get('height', 1024),
        'crop': kwargs.get('cropType', 'mfit')
    }
    time_stamp = int(datetime.timestamp(datetime.now()))

    try:
        res = cloudinary.uploader.upload(file_path,
                                         folder=settings.CLOUDINARY_FOLDER,
                                         tags=settings.CLOUDINARY_DEFAULT_TAGS,
                                         public_id=time_stamp,
                                         allowed_formats=['jpg', 'png'],
                                         eager=[eager])
        if res and not is_async:
            return res

        logger.info(f'Uploaded image: {res["secure_url"]}')

    except Exception as e:
        logger.error(f'Could not upload image: {e}')
        return ResponseHandler.raise_error({'file': e})


@shared_task(name='delete-image')
def delete_image(public_id):
    """Method to Delete image file to cloudinary."""
    try:
        cloudinary.uploader.destroy(public_id)
        logger.info(f'Deleted image')

    except Exception as e:
        logger.error(f'Could not deleter image: {e}')
        return ResponseHandler.raise_error({'image': e})
