import datetime

from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import BoardTask


class TaskForm(forms.ModelForm):
    """
    Form to add a new task in the personal board.
    """

    class Meta:
        model = BoardTask
        fields = '__all__'

        widget_date_attrs = {
            'class': 'form-control',
            'value': datetime.datetime.now().strftime("%Y-%m-%d"),
            'placeholder': 'Select a date',
            'type': 'date'}

        widget_time_attrs = {
            'class': 'form-control',
            'value': datetime.datetime.now().strftime("%H:%M"),
            'type': 'time'}

        widgets = {
           'task_comment': forms.Textarea(attrs={'cols': 20, 'rows': 5}),
           'task_start_date': forms.DateInput(format="%Y-%m-%d", attrs=widget_date_attrs),
           'task_end_date': forms.DateInput(format="%Y-%m-%d", attrs=widget_date_attrs),
           'task_start_time': forms.TimeInput(format="%H:%M", attrs=widget_time_attrs),
           'task_end_time': forms.TimeInput(format="%H:%M", attrs=widget_time_attrs),
           'task_rating': forms.NumberInput(attrs={'min': '0', 'max': '10', 'type': 'number'})
        }

        error_messages = {
            'task_comment': {
                'max_length': _("This comment is too long."),
            },
        }


class TaskDoneForm(forms.ModelForm):
    class Meta:
        model = BoardTask
        fields = ["task_done"]