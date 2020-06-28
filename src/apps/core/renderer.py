"""Custom Django renderer"""
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from src.apps.core.utils import ResponseHandler


class CustomJSONRenderer(CamelCaseJSONRenderer):
    """Custom renderer"""
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        
        Args:
            data:
            accepted_media_type:
            renderer_context:

        Returns:

        """
        response = renderer_context.get('response')
        if response.status_code == 404:
            data = ResponseHandler.response({}, key='USR_04', status='error')
        elif response.status_code >= 400:
            data = ResponseHandler.response(data, key='USR_O3', status='error')
        else:
            data = ResponseHandler.response(data)
        return super(CustomJSONRenderer,
                     self).render(data, accepted_media_type, renderer_context)
