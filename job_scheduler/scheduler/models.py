import calendar

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Worker(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Month(models.Model):
    year = models.PositiveIntegerField()
    month_number = models.PositiveIntegerField(choices=[(i, calendar.month_name[i]) for i in range(1, 13)])

    class Meta:
        unique_together = ('year', 'month_number')

    def __str__(self):
        return f"{self.month_number} {self.year}"


class Day(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    day_number = models.PositiveIntegerField(validators=[MaxValueValidator(31), MinValueValidator(1)], )
    workers_required = models.PositiveIntegerField()
    workers = models.ManyToManyField(Worker)

    def __str__(self):
        return f'Day {self.day_number} in {self.month}'
