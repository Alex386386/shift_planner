import calendar

from rest_framework import mixins
from rest_framework import viewsets

MAX_NUMBER_SHIFTS: int = 12


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


def required_workers_for_days(month, year):
    _, days_in_month = calendar.monthrange(year, month)

    day_workers = {}
    for day in range(1, days_in_month + 1):
        weekday = calendar.weekday(year, month, day)
        if weekday == 0:
            day_workers[day] = 3
        elif weekday == 6:
            day_workers[day] = 1
        else:
            day_workers[day] = 2

    return day_workers
