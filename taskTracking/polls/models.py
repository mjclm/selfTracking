import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


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
    task_start_date = models.DateTimeField('start task')
    task_end_date = models.DateTimeField('end task')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    task_comment = models.CharField(max_length=140)
    task_rating = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )

    def do_something(self):
        pass

    def __str__(self):
        return self.task.task_name
