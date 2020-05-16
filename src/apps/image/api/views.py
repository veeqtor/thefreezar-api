"""Views"""
from rest_framework.response import Response
from rest_framework import generics, status

from src.apps.core.utils.decorators import validate_id
from src.apps.core.utils.messages import ERRORS
from src.apps.core.utils.response import ResponseHandler
from src.apps.image.models import Image
from src.apps.image.utils.upload import upload_image_file
from src.apps.image.api.serializers import ImageSerializer


class ImageListCreateView(generics.ListCreateAPIView):
    """
    A ViewSet for viewing and editing accounts.
    """
    serializer_class = ImageSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs) -> object:
        """
        Getting the all images.
        """
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        response = ResponseHandler.response(serializer.data)
        return Response(response)

    def post(self, request, *args, **kwargs) -> object:
        """
        Uploading an image to cloudinary.
        Args:
            request:
            *args:
            **kwargs:

        Returns:
        """
        try:
            file_obj = request.FILES['file']
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            instance = Image.objects.filter(pk=data.get('id')).first()

            if instance:
                image_res = upload_image_file(file_obj, is_async=False)
                instance.image_public_id = image_res.get('public_id')
                instance.image_url = image_res.get('secure_url')
                instance.save()
                serializer = self.get_serializer(instance)
                response = ResponseHandler.response(serializer.data)
                return Response(response, status=status.HTTP_201_CREATED)

        except KeyError:
            return ResponseHandler.raise_error(ERRORS['FILE_03'])

    def get_queryset(self):
        """
        Get queryset for image
        """
        return Image.objects.filter(is_deleted=False).all()


class ImageRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """
    Class representing view detail and destroy.
    """

    serializer_class = ImageSerializer
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        """Get an image"""

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = ResponseHandler.response(serializer.data)
        return Response(response)

    def destroy(self, request, *args, **kwargs):
        """Delete an image"""

        instance = self.get_object()
        self.perform_destroy(instance)
        response = ResponseHandler.response({'data': 'Deleted.'})
        return Response(response)

    @validate_id
    def get_object(self):
        """
        Get the object
        """
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            return queryset.filter(**filter_kwargs).get()
        except Image.DoesNotExist:
            return ResponseHandler.raise_error(
                ERRORS['USR_04'], status_code=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        """
        Get queryset for image
        """
        return Image.objects.filter(is_deleted=False).all()
