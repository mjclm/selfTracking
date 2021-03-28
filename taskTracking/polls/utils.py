import datetime
from .models import BoardTask

from django.db.models import F, ExpressionWrapper, fields
from django.db.models import Count, Sum


def date_from_str_to_datetime(date: str) -> datetime.datetime:
    date_split = tuple(map(int, date.split("-")))  # split date
    return datetime.datetime(*date_split)


def timedelta_to_seconds(timedelta: datetime.timedelta) -> int:
    return timedelta.seconds
