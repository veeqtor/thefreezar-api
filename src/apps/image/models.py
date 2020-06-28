"""Model"""

from django.db import models
from src.apps.core.models import BaseAuditableModel
from src.apps.studio_session.models import StudioSession


class Image(BaseAuditableModel):
    """Image model."""

    SAMPLE_IMAGE = '0'
    USER_IMAGE = '1'
    SERVICES_IMAGE = '2'

    IMAGE_TYPE_CHOICES = ((SAMPLE_IMAGE, 'Sample Image'),
                          (USER_IMAGE, 'User\'s Image'), (SERVICES_IMAGE,
                                                          'Service\'s Image'))

    image_type = models.CharField('Image Type',
                                  max_length=30,
                                  choices=IMAGE_TYPE_CHOICES,
                                  default=SAMPLE_IMAGE)
    is_public = models.BooleanField('Public Image', default=False)
    is_hero_bg = models.BooleanField('Use as Hero Background', default=False)
    image_url = models.CharField("Image url",
                                 max_length=200,
                                 blank=False,
                                 null=False)
    image_public_id = models.CharField("Image id",
                                       max_length=200,
                                       blank=False,
                                       null=False)
    studio_session_image = models.ForeignKey(
        StudioSession,
        related_name='studio_session_image',
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    @property
    def image_type_str(self):
        """String rep for image type"""
        for choice in self.IMAGE_TYPE_CHOICES:
            if str(choice[0]) == self.image_type:
                return choice[1]

    class Meta:
        """Meta"""
        verbose_name_plural = 'Images'
        db_table = 'images'

    def __str__(self):
        """ Informative name for model """

        return f"Photo <{self.image_type_str}:{self.image_public_id}>"
