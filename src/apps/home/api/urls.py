"""Viewset for home view"""

from src.apps.home.api.views import HomeAPIView
from django.urls import path

urlpatterns = [
    path('', HomeAPIView.as_view(), name='homepage'),
]
