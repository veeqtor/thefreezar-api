"""urls"""
from src.apps.image.api.views import (ImageListCreateView,
                                      ImageRetrieveDestroyView)
from django.urls import path, re_path

urlpatterns = [
    path('', ImageListCreateView.as_view(), name='image-list'),
    re_path(r'(?P<pk>[\w-]+)',
            ImageRetrieveDestroyView.as_view(),
            name='image-detail'),
]
