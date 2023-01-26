from enum import Enum

from django_celery_beat.models import IntervalSchedule


class TimeInterval(Enum):
    five_sec = '5 sec'
    thirty_sec = '30 sec'
    one_min = '1 min'
    three_min = '3 mins'
    five_min = '5 mins'
    ten_min = '10 mins'
    thirty_min = '30 mins'
    one_hour = '1 hour'


class TaskStatus(Enum):
    active = 'Active'
    disabled = 'Disabled'


def get_time_interval(time: str):
    # 30 seconds
    if time is TimeInterval.thirty_sec:
        return IntervalSchedule.objects.get(every=30, period='seconds')
    # 1 minute
    if time is TimeInterval.one_min:
        return IntervalSchedule.objects.get(every=1, period='minutes')
    # 3 minutes
    if time is TimeInterval.three_min:
        return IntervalSchedule.objects.get(every=3, period='minutes')
    # 5 minutes
    if time is TimeInterval.five_min:
        return IntervalSchedule.objects.get(every=5, period='minutes')
    # 10 minutes
    if time is TimeInterval.ten_min:
        return IntervalSchedule.objects.get(every=10, period='minutes')
    # 30 minutes
    if time is TimeInterval.thirty_min:
        return IntervalSchedule.objects.get(every=30, period='minutes')
    # 1 hour
    if time is TimeInterval.one_hour:
        return IntervalSchedule.objects.get(every=1, period='hours')
    raise NotImplementedError