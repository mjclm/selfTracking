import datetime

from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import BoardTask


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        pass


class TaskForm(forms.ModelForm):
    class Meta:
        model = BoardTask
        fields = "__all__"

        widget_date_attrs = {
            'class': 'form-control',
            'value': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'placeholder': 'Select a date',
            'type': 'datetime-local'}

        widgets = {
           'task_comment': forms.Textarea(attrs={'cols': 20, 'rows': 5}),
           'task_start_date': forms.DateTimeInput(format="%Y-%m-%d %H:%M:%S", attrs=widget_date_attrs),
           'task_end_date': forms.DateTimeInput(format="%Y-%m-%d %H:%M:%S", attrs=widget_date_attrs),
           'task_rating': forms.NumberInput(attrs={'min': '0', 'max': '10', 'type': 'number'})
        }

        error_messages = {
            'task_comment': {
                'max_length': _("This comment is too long."),
            },
        }

