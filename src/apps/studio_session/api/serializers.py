"""Serializer"""
from datetime import timedelta
from random import uniform

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.apps.core.utils import ResponseHandler
from src.apps.core.utils.messages import ERRORS
from src.apps.studio_session import models
from src.apps.studio_session.utils import (get_localized_slots,
                                           is_duration_available)


class StudioSessionTypeSerializer(serializers.ModelSerializer):
    """Class representing the studio session type serializer"""
    class Meta:
        """Meta class"""

        model = models.StudioSessionType
        fields = ('id', 'name', 'price', 'max_duration')


class StudioSessionSerializerWithSessionType(serializers.ModelSerializer):
    """Class representing the studio session serializer"""

    packages = StudioSessionTypeSerializer(source='studio_session_type',
                                           many=True)
    images = serializers.SerializerMethodField()
    image_fade_multiplier = serializers.SerializerMethodField()

    class Meta:
        """Meta class"""

        model = models.StudioSession
        fields = ('id', 'name', 'description', 'packages', 'images',
                  'image_fade_multiplier')

    def get_image_fade_multiplier(self, instance):
        """Adds a multiplier for image fades"""
        return uniform(1, 2)

    def get_images(self, instance):
        """Get images for this session"""
        images = instance.studio_session_image.all().values_list('image_url',
                                                                 flat=True)
        if not images:
            images = [
                'https://images.pexels.com/photos/3561145/pexels-photo-3561145.jpeg?cs=srgb&dl=portrait-photography-of-beautiful-woman-3561145.jpg&fm=jpg',
                'https://images.pexels.com/photos/3886337/pexels-photo-3886337.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500',
            ]
        return images


class StudioSessionSerializer(serializers.ModelSerializer):
    """Class representing the studio session serializer"""
    class Meta:
        """Meta class"""

        model = models.StudioSession
        fields = ('id', 'name', 'description')


class StudioSessionCoordinatorSerializer(serializers.ModelSerializer):
    """Class representing the studio session coordinator serializer"""

    slots = serializers.SerializerMethodField()

    class Meta:
        """Meta class"""

        model = models.StudioSessionCoordinator
        fields = ('id', 'start_of_day', 'end_of_day', 'break_start_time',
                  'break_duration', 'is_available', 'user', 'slots')

    def get_slots(self, instance):
        """Gets localized slots"""
        day = self.context['request'].query_params.get('date', None)
        if day:
            return get_localized_slots(instance, day)
        return get_localized_slots(instance)


class StudioSessionReservationSerializer(serializers.ModelSerializer):
    """Class representing the studio session reservation serializer"""
    coordinator = StudioSessionCoordinatorSerializer(read_only=True)
    session_type = StudioSessionTypeSerializer(read_only=True)
    session = StudioSessionSerializer(source='session_type.studio_session',
                                      read_only=True,
                                      required=False)

    class Meta:
        """Meta class"""

        model = models.StudioSessionReservation
        fields = ('id', 'status', 'duration', 'reservation_datetime',
                  'reservation_end_datetime', 'session_type', 'session',
                  'coordinator', 'user')


class StudioSessionReservationCreateSerializer(serializers.ModelSerializer):
    """Class representing the studio session reservation serializer"""

    coordinator = serializers.PrimaryKeyRelatedField(
        queryset=models.StudioSessionCoordinator.objects.filter(
            is_deleted=False).all())
    session_type = serializers.PrimaryKeyRelatedField(
        queryset=models.StudioSessionType.objects.filter(
            is_deleted=False).all())

    class Meta:
        """Meta class"""

        model = models.StudioSessionReservation
        fields = ('id', 'status', 'duration', 'reservation_datetime',
                  'reservation_end_datetime', 'session_type', 'coordinator',
                  'user')

    def validate(self, attrs):
        """Extra validations for session reservation"""

        user = attrs.get('user')
        coordinator = attrs.get('coordinator')
        studio_session_type = attrs.get('session_type')
        reservation_datetime = attrs.get('reservation_datetime')
        attrs['duration'] = studio_session_type.max_duration
        reservation_end_datetime = reservation_datetime + \
                                   timedelta(minutes=attrs['duration'] - 5)
        if user == coordinator.user:
            raise ValidationError(ERRORS['SESS_01'])

        available_slots = get_localized_slots(
            coordinator, reservation_datetime.strftime('%Y-%m-%d'))
        is_valid = is_duration_available(reservation_datetime,
                                         reservation_end_datetime,
                                         available_slots)

        if not is_valid:
            # TODO: create an algorithm to suggest the next availabale time
            #  slots for the choosen duration
            raise ValidationError(ERRORS['SESS_02'])

        return attrs
