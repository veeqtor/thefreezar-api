"""Home Model Serializers"""

from rest_framework import serializers
from src.apps.home import models
from src.apps.image.api.serializers import ImageSerializer


class HeroImageSerializer(serializers.ModelSerializer):
    """Class representing the Hero image serializer"""

    hero_image = ImageSerializer()

    class Meta:
        """Meta class"""

        model = models.HeroImage
        fields = ('id', 'hero_caption', 'hero_image')


class PortfolioImageSerializer(serializers.ModelSerializer):
    """Class representing the Portfolio image serializer"""

    portfolio_image = ImageSerializer()

    class Meta:
        """Meta class"""

        model = models.PortfolioImage
        fields = ('id', 'portfolio_description', 'portfolio_image')
