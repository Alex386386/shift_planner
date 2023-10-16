import math

from django.db.models import Prefetch
from rest_framework import (
    viewsets,
    status,
)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response

from scheduler.models import (
    Month,
    Day,
    Worker,
)
from .serializers import (
    MonthSerializer,
    WorkerSerializer,
)
from .utils import (
    required_workers_for_days,
    CreateListRetrieveViewSet,
    MAX_NUMBER_SHIFTS,
)


class WorkerViewSet(CreateListRetrieveViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = (IsAuthenticated,)


class MonthViewSet(viewsets.ModelViewSet):
    queryset = Month.objects.all().prefetch_related(
        Prefetch('day_set', queryset=Day.objects.prefetch_related('workers'))
    )
    serializer_class = MonthSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        month_instance = serializer.save()

        self.assign_workers_for_month(month_instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def assign_workers_for_month(self, month_instance):
        """Функция создания дней для месяца, и запись минимального количества работников для рабочего дня."""
        day_workers = required_workers_for_days(month_instance.month_number, month_instance.year)
        workers = Worker.objects.all().order_by('?')
        shifts_worked = {worker: 0 for worker in workers}

        for day, workers_required in day_workers.items():
            day_instance = Day.objects.create(month=month_instance, day_number=day, workers_required=workers_required)
            self.assign_workers_for_day(day_instance, shifts_worked)
        self.adjust_for_weekends(month_instance, shifts_worked)

    def assign_workers_for_day(self, day_instance, shifts_worked):
        """Добавление сотрудников в рабочий день."""
        sorted_workers = sorted(shifts_worked, key=lambda k: shifts_worked[k])
        workers_in_day = len(sorted_workers) / 3
        workers_in_day = math.ceil(workers_in_day)
        for worker in sorted_workers[:workers_in_day]:
            day_instance.workers.add(worker)
            shifts_worked[worker] += 1

    def adjust_for_weekends(self, month_instance, shifts_worked):
        """Обработка исключений, запись сотрудников в понедельники и воскресенья."""
        mondays = month_instance.day_set.filter(workers_required=3).prefetch_related('workers')
        sundays = month_instance.day_set.filter(workers_required=1).prefetch_related('workers')

        for sunday in sundays:
            sunday_worker = sunday.workers.first()
            if len(sunday.workers.all()) > 1:
                sunday.workers.remove(sunday_worker)
                shifts_worked[sunday_worker] -= 1

        for monday in mondays:
            sorted_workers = sorted(shifts_worked, key=lambda k: shifts_worked[k])
            for worker in sorted_workers:
                if worker not in monday.workers.all() and shifts_worked[worker] < MAX_NUMBER_SHIFTS:
                    monday.workers.add(worker)
                    shifts_worked[worker] += 1
                    break
