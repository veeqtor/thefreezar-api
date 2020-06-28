"""Pagination"""

from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response

from src.apps.core.utils import ResponseHandler


class Pagination(pagination.PageNumberPagination):
    """Custom pagination"""
    def get_paginated_response(self, data):
        """Custom pagination response"""

        response = {
            'results':
            data,
            'meta':
            OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
            ])
        }

        return Response(response)
