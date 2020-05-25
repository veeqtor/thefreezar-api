"""Admin"""

from django.contrib import admin

from src.apps.image import models

admin.site.register(models.Image)
