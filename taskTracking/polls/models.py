import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here

class Task(models.Model):
    task_name = models.CharField(max_length=50)
    task_category = models.CharField(max_length=50)
    task_short_description = models.CharField(max_length=140)
    task_added_date = models.DateTimeField('date added')

    def is_new_task(self):
        now = timezone.now()
        return now - datetime.timedelta(months=1) <= self.task_added_date <= now

    def __str__(self):
        return self.task_name


class BoardTask(models.Model):
    task_start_date = models.DateField('start date task')
    task_end_date = models.DateField('end date task')
    task_start_time = models.TimeField('start time task')
    task_end_time = models.TimeField('end time task')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    task_comment = models.CharField(max_length=140)
    task_rating = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    task_done = models.BooleanField(default=False)

    def do_something(self):
        pass

    def __str__(self):
        return self.task.task_name
