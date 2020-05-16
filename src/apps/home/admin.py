"""Admin"""

from django.contrib import admin
from src.apps.home import models

admin.site.register(models.HeroImage)
admin.site.register(models.PortfolioImage)
