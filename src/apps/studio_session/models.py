"""Sessions Model"""
from datetime import timedelta
from django.db import models
from django.utils.functional import cached_property

from src.apps.core.models import BaseAuditableModel
from src.apps.core.utils import date_validator
from src.apps.user.models import User
from src.apps.studio_session.utils import (get_datetime_and_capacity,
                                           generate_slots, filter_slots,
                                           localize_datetime, INTERVAL)


class StudioSession(BaseAuditableModel):
    """Studio Session model."""

    name = models.CharField("Name ", max_length=200, blank=False, null=False)
    description = models.TextField('Studio Session description',
                                   max_length=400,
                                   blank=False,
                                   null=False)

    class Meta:
        """Meta"""
        verbose_name_plural = 'Studio Sessions'
        db_table = 'st_sessions'

    def __str__(self):
        """ Informative name for model """
        return f"Studio Session <{self.name}>"


class StudioSessionType(BaseAuditableModel):
    """Studio Session types model."""

    name = models.CharField("Name ", max_length=200, blank=False, null=False)
    price = models.FloatField("Price ", blank=False, null=False, default=0.00)
    max_duration = models.IntegerField('Maximum duration',
                                       default=30,
                                       blank=False,
                                       null=False)
    studio_session = models.ForeignKey(StudioSession,
                                       related_name='studio_session_type',
                                       on_delete=models.DO_NOTHING,
                                       blank=False,
                                       null=False)

    class Meta:
        """Meta"""
        verbose_name_plural = 'Studio Session Type'
        db_table = 'st_session_types'

    def __str__(self):
        """ Informative name for model """
        return f"Studio Session type <{self.name} - type:{self.price}>"


class StudioSessionCoordinator(BaseAuditableModel):
    """Studio Session Coordinator model"""

    start_of_day = models.TimeField('Start time for the day',
                                    null=False,
                                    blank=False)
    end_of_day = models.TimeField('End time for the day',
                                  null=False,
                                  blank=False)

    break_start_time = models.TimeField('Daily break time',
                                        null=False,
                                        blank=False)
    break_duration = models.IntegerField('Daily Break duration',
                                         blank=False,
                                         null=False,
                                         default=60)
    is_available = models.BooleanField('Coordinator\'s availability',
                                       default=True)

    user = models.ForeignKey(User,
                             related_name='studio_session_coordinator',
                             blank=False,
                             null=False,
                             on_delete=models.CASCADE)

    @cached_property
    def slots(self):
        """All slots for this coordinator"""
        return self.get_slots_by_date()

    def get_slots_by_date(self, day=None):
        """Get all slots for the coordinator
        
        Args:
            day (string): date string '2020-05-12'

        Returns:

        """
        validated_date = None
        if day:
            validated_date = date_validator(day)

        capacity, start, end = get_datetime_and_capacity(
            self.start_of_day,
            self.end_of_day,
            INTERVAL,
            for_date=validated_date)
        slots = generate_slots(start, capacity, INTERVAL)
        filtered_slots = filter_slots(INTERVAL,
                                      self.assigned_reservations.all(), slots)
        return filtered_slots

    class Meta:
        """Meta"""
        verbose_name_plural = 'Studio Session Coordinator'
        db_table = 'st_session_coordinators'

    def __str__(self):
        """ Informative name for model """

        return f"Studio Session Coordinator<{self.user.email}>"


class StudioSessionReservation(BaseAuditableModel):
    """Studio Session reservation model."""

    PENDING = '0'
    CONFIRMED = '1'
    ARRIVED = '2'
    CANCELLED = '3'
    DONE = '4'

    STATUS_CHOICES = ((PENDING, 'Pending'), (CONFIRMED, 'Confirmed'),
                      (ARRIVED, 'Arrived'), (CANCELLED, 'Cancelled'), (DONE,
                                                                       'Done'))

    status = models.CharField('Reservation Status',
                              max_length=30,
                              choices=STATUS_CHOICES,
                              default=PENDING)

    reservation_datetime = models.DateTimeField('Reservation datetime')
    user = models.ForeignKey(User,
                             related_name='studio_sessions',
                             on_delete=models.CASCADE)
    session_type = models.ForeignKey(StudioSessionType,
                                     related_name='session_type',
                                     on_delete=models.CASCADE,
                                     null=False,
                                     blank=False)
    duration = models.IntegerField('Session duration',
                                   default=30,
                                   blank=False,
                                   null=False)
    coordinator = models.ForeignKey(StudioSessionCoordinator,
                                    blank=False,
                                    related_name='assigned_reservations',
                                    null=False,
                                    on_delete=models.CASCADE)

    @cached_property
    def reservation_end_datetime(self):
        """The end datetime for the reservation"""

        return localize_datetime(self.reservation_datetime +
                                 timedelta(minutes=self.duration))

    class Meta:
        """Meta"""
        verbose_name_plural = 'Studio Session Reservation'
        db_table = 'st_session_reservations'

    def __str__(self):
        """ Informative name for model """
        return f"Studio Session Reservation<{self.user.email} -" \
               f" {self.session_type.name}>"
