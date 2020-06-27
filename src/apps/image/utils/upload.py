"""Interface for uploading images"""

from django.conf import settings
import PIL
from PIL import Image

from src.apps.core.utils.messages import ERRORS
from src.apps.core.utils.response import ResponseHandler
from src.apps.core.tasks import upload_image, delete_image


def validate_image_file(image_file_obj):
    """Image file validations"""

    try:
        image = Image.open(image_file_obj)
        if image_file_obj.size > settings.MAX_IMAGE_SIZE:
            return ResponseHandler.raise_error(ERRORS['FILE_01'])

        path = image_file_obj.temporary_file_path()
        return image, path

    except (IOError, FileNotFoundError, ValueError,
            PIL.UnidentifiedImageError) as e:

        exception_mapper = {
            IOError: ERRORS['FILE_02'],
            FileNotFoundError: ERRORS['FILE_03'],
            ValueError: ERRORS['FILE_02'],
            PIL.UnidentifiedImageError: ERRORS['FILE_04']
        }
        return ResponseHandler.raise_error(exception_mapper.get(type(e)))


def upload_image_file(file, is_async=True):
    """Method to upload image file."""

    image, file_path = validate_image_file(file)
    return upload_image.delay(file_path, is_async) \
        if is_async else upload_image(file_path, is_async)


def delete_image_file(public_id, is_async=True):
    """Method to upload image file."""

    return delete_image.delay(public_id) \
        if is_async else delete_image(public_id)
