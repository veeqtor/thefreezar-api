"""Studio session Utils"""

import copy
from datetime import datetime, date, timedelta

from dateutil import tz
from django.conf import settings

from src.apps.core.utils import date_validator

local_tz = tz.gettz(settings.TIME_ZONE)
utc = tz.UTC
INTERVAL = settings.STUDIO_SESSION_INTERVAL


def localize_datetime(datetime):
    """Localize dates"""
    return datetime.astimezone(tz=local_tz)


def convert_to_utc(localized_datetime):
    """Convert datetime to utc"""
    return localized_datetime.astimezone(tz=utc)


def get_datetime_and_capacity(start, end, interval, for_date=None):
    """Gets the start, end datetime and the slot capacity for the day

    Args:
        start (datetime.time): Start time for the day
        end (datetime.time): End time for the day
        for_date (date): Date
        interval (int): The session intervals in minutes

    Returns:
        capacity (int): The max capacity for the day.
        start_datetime (datetime): The start datetime in UTC
        end_datetime (datetime): The end datetime in UTC
    """

    today = date.today()
    if for_date:
        today = for_date

    end_time = end.replace(tzinfo=local_tz)
    start_time = start.replace(tzinfo=local_tz)
    start_datetime = (datetime.combine(today, start_time)).astimezone(tz=utc)
    end_datetime = (datetime.combine(today, end_time)).astimezone(tz=utc)
    work_hour_delta = end_datetime - start_datetime
    capacity = work_hour_delta // timedelta(minutes=interval)
    return capacity, start_datetime, end_datetime


def generate_slots(start, capacity, interval):
    """This generates all slots for the day based on the start datetime,
    capacity for the day and the intervals between sessions.

    Args:
        start (datetime): The start datetime in UTC
        capacity (int): The max capacity for the day.
        interval (int): The session intervals in minutes

    Returns:
        arr (Array): An array of objects containing all slots and datetime
    """

    arr = []
    curr = start
    i = 0
    while i != capacity:
        next_datetime = curr + timedelta(minutes=interval)
        # TODO: Add more checks to determine if a slot is available for booking
        if datetime.now(tz=utc) < curr:
            arr.append({'datetime': curr, 'available': True})
        i += 1
        curr = next_datetime
    return arr


def filter_slots(interval, reserved_sessions, slots):
    """Modifies the slots to indicate which is available or not.

    Args:
        interval (int): The session intervals in minutes
        reserved_sessions (SessionReservation): All reserved session for the day.
        slots (list): Array of slots.

    Returns:
        filtered slots (Array): Updated Array of slots with proper availability
        modified.
    """
    slots_copy = copy.deepcopy(slots)
    for session in reserved_sessions:
        try:
            dt = session.reservation_datetime
            while dt <= session.reservation_end_datetime:
                slot = next(filter(lambda x: x['datetime'] == dt, slots_copy))
                if slot:
                    slot['available'] = False
                dt = dt + timedelta(minutes=interval)
        except StopIteration:
            pass

    return slots_copy


def filter_out_break_time(interval, preferred_coordinator, day=None):
    """This method filter out the break times out of the coordinators slot.
    
    Args:
        interval (int): The session intervals in minutes
        preferred_coordinator (StudioSessionCoordinator): The Studio
        Session Coordinator instance
        day (string): The date_value

    Returns:
        filtered slots (Array): Updated slot array accounting for breaktimes.
    """
    validated_day = date.today()
    if day:
        validated_day = date_validator(day)
    start_time = preferred_coordinator.break_start_time.replace(
        tzinfo=local_tz)
    start_datetime = (datetime.combine(validated_day, start_time)) \
        .astimezone(tz=utc)
    end_datetime = start_datetime + \
                   timedelta(minutes=preferred_coordinator.break_duration)
    slots = preferred_coordinator.get_slots_by_date(day)
    for slot in slots:
        dt = start_datetime
        while dt <= end_datetime:
            if slot['datetime'] == dt:
                slot['available'] = False
            dt = dt + timedelta(minutes=interval)
    return slots


def filter_and_convert_to_localtime(slots):
    """
    Filters available slots and converts the date time
    to the local timezone
    """
    return list(
        map(lambda x: localize_datetime(x['datetime']),
            filter(lambda x: x['available'], slots)))


def get_localized_slots(instance, day=None):
    """Gets the filtered localized slot datetime
    """
    # Removing the coordinators break period from the available slots
    slots = filter_out_break_time(INTERVAL, instance, day)
    return filter_and_convert_to_localtime(slots)


def is_duration_available(start, end, slots):
    """
    Checks that the coordinator can accommodate the duration
    
    Args:
        start (datetime): The start datetime
        end (datetime): The end datetime
        slots (list): A list of available slots

    Returns:
        bool
    """

    is_valid = True
    try:
        found = next(filter(lambda x: x == start, slots))
        if found:
            while start <= end:
                exist = any(slot == start for slot in slots)
                if not exist:
                    is_valid = False
                    break
                start = start + timedelta(minutes=INTERVAL)
    except StopIteration:
        is_valid = False
    return is_valid
