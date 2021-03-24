from datetime import datetime


def date_from_str_to_datetime(date: str) -> datetime:
    date_split = tuple(map(int, date.split("-")))  # split date
    return datetime(*date_split)
