"""Admin"""

from django.contrib import admin
from src.apps.studio_session import models

admin.site.register(models.StudioSession)
admin.site.register(models.StudioSessionType)
admin.site.register(models.StudioSessionCoordinator)
admin.site.register(models.StudioSessionReservation)
