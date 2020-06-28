"""Views"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins

from src.apps.core.utils.messages import ERRORS
from src.apps.core.utils.response import ResponseHandler
from src.apps.studio_session.api import serializers
from src.apps.studio_session import models


class StudioSessionViewSet(ModelViewSet):
    """ViewSet for studio sessions"""

    permission_classes = (AllowAny, )
    serializer_class = serializers.StudioSessionSerializerWithSessionType

    def get_queryset(self):
        """Queryset for the studio session"""

        return models.StudioSession.objects.filter(
            is_deleted=False).order_by('id').all()


class StudioSessionCoordinatorViewSet(GenericViewSet, mixins.CreateModelMixin,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin):
    """ViewSet for studio sessions coordinator"""

    permission_classes = (AllowAny, )
    serializer_class = serializers.StudioSessionCoordinatorSerializer

    @action(detail=False)
    def preferred(self, request):
        """
        Get the preferred slots for the day.
        This is based on the coordinator with most free slots.
        while putting into account break time.
        """
        day = request.query_params.get('date', None)
        preferred_coordinator = None
        number_of_available_slots = 0

        if day is None:
            return ResponseHandler.raise_error(
                ERRORS['SESS_03'], status_code=status.HTTP_400_BAD_REQUEST)

        # TODO: modify the algo to compensate for coordinators level of
        #  experience, session type and coordinators ratings. for now it just
        #  gets the coordinator with the most free slots
        for qs in self.get_queryset():
            slots = qs.get_slots_by_date(day)
            max_slot = 0
            i = 0
            while i < len(slots):
                if slots[i]['available']:
                    max_slot += 1
                i += 1
            if max_slot > number_of_available_slots:
                number_of_available_slots = max_slot
                # This coordinator has the most free slots
                preferred_coordinator = qs

        if preferred_coordinator:
            serializer = self.get_serializer(preferred_coordinator)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_200_OK)

    def get_queryset(self):
        """Queryset for the studio sessions coordinator"""

        return models.StudioSessionCoordinator.objects \
            .filter(is_deleted=False).order_by('id').all()


class StudioSessionReservationViewSet(ModelViewSet):
    """ViewSet for studio sessions reservation"""

    permission_classes = (AllowAny, )
    serializer_class = serializers.StudioSessionReservationSerializer

    def create(self, request, *args, **kwargs):
        """Make a reservation"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """Queryset for the studio sessions coordinator"""
        return models.StudioSessionReservation.objects \
            .filter(is_deleted=False).order_by('id').all()

    def get_serializer_class(self):
        """Gets the appropriate class for serialization"""
        if self.action in ['create']:
            return serializers.StudioSessionReservationCreateSerializer
        return super().get_serializer_class()
