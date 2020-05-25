"""Model"""

from django.db import models
from src.apps.core.models import BaseAuditableModel
from src.apps.image.models import Image


class HeroImage(BaseAuditableModel):
    """Hero Image model."""

    hero_caption = models.CharField('Hero Caption',
                                    max_length=20,
                                    null=False,
                                    blank=False)
    hero_image = models.OneToOneField(Image,
                                      on_delete=models.CASCADE,
                                      related_name='hero_image')

    class Meta:
        """Meta"""
        verbose_name_plural = 'Hero Images'
        db_table = 'hero_images'

    def __str__(self):
        """ Informative name for model """
        return f"Hero Caption: <{self.hero_caption}>"


class PortfolioImage(BaseAuditableModel):
    """Portfolio Image model."""

    portfolio_description = models.CharField('Portfolio Desc.',
                                             max_length=20,
                                             blank=True,
                                             null=True)
    portfolio_image = models.OneToOneField(Image,
                                           on_delete=models.CASCADE,
                                           related_name='portfolio_image')

    class Meta:
        """Meta"""
        verbose_name_plural = 'Portfolio Images'
        db_table = 'portfolio_images'

    def __str__(self):
        """ Informative name for model """
        return f"Portfolio Caption: <{self.portfolio_description}>"
