"""Home API"""

from rest_framework import views
from rest_framework.response import Response

from src.apps.home import models
from src.apps.home.api import serializers
from src.apps.image.models import Image


class HomeAPIView(views.APIView):
    """Class for home view"""

    permission_classes = []

    def get(self, request, *args, **kwargs):
        """List out all image for the homepage."""

        hero_qs = models.HeroImage.objects.filter(
            hero_image__is_deleted=False,
            hero_image__is_hero_bg=True,
            hero_image__is_public=True,
            hero_image__image_type=Image.SAMPLE_IMAGE).all()

        portfolio_qs = models.PortfolioImage.objects.filter(
            portfolio_image__is_deleted=False,
            portfolio_image__is_public=True,
            portfolio_image__image_type=Image.SAMPLE_IMAGE).all()

        hero = serializers.HeroImageSerializer(hero_qs, many=True)
        portfolio = serializers.PortfolioImageSerializer(portfolio_qs,
                                                         many=True)
        response = {'hero': hero.data, 'portfolio': portfolio.data}
        return Response(response)
