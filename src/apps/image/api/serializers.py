"""Image Serializers"""

from rest_framework import serializers
from src.apps.image import models


class ImageSerializer(serializers.ModelSerializer):
    """Class representing the image serializer"""
    class Meta:
        """Meta class"""

        model = models.Image
        fields = ('id', 'image_type_str', 'is_hero_bg', 'image_type',
                  'is_public', 'image_url', 'image_public_id')
        read_only_fields = ('image_type_str', 'image_url', 'image_public_id')
