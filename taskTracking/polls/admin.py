from django.contrib import admin

from .models import Task, BoardTask


admin.site.register(Task)
admin.site.register(BoardTask)
