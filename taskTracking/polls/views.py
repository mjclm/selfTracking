from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.translation import ugettext as _

from .models import BoardTask, Task
from .forms import TaskForm

from .utils import date_from_str_to_datetime


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'polls/index.html'


class AboutView(generic.TemplateView):
    template_name = "polls/about.html"
    context_object_name = 'latest_tasks_list'


class TimeTableView(generic.TemplateView):
    template_name = 'polls/timetable.html'

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        date_range = (date_from_str_to_datetime(request.GET.get("visual_start_date", now.strftime("%Y-%m-%d"))),
                      date_from_str_to_datetime(request.GET.get("visual_end_date", (now + timezone.timedelta(days=7)).strftime("%Y-%m-%d"))))

        self.object_list = self.get_queryset(date_range)

        context = self.get_context_data(object_list=self.object_list)

        return self.render_to_response(context)

    def get_queryset(self, date_range):
        start_date, end_date = date_range
        return BoardTask.objects.filter(task_start_date__range=(start_date, end_date)).order_by("task_start_time")


class TaskView(generic.edit.FormView):
    template_name = 'polls/task_input.html'
    form_class = TaskForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect(reverse('polls:timetable'))

        return render(request, self.template_name, {'form': form})


class TaskModifyView(generic.edit.FormView):
    template_name = 'polls/task_input.html'
    form_class = TaskForm

    def post(self, request, *args, **kwargs):
        instance = BoardTask.objects.get(pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect(reverse('polls:timetable'))

        return render(request, self.template_name, {'form': form})

    def get_initial(self, *args, **kwargs):
        """
        Returns the initial data to use for forms on this view
        """
        initial = super().get_initial()
        some_object = BoardTask.objects.filter(pk=self.kwargs['pk']).values()[0]
        print(some_object)
        initial.update(some_object)
        initial.update({'task': Task.objects.get(pk=some_object.get('task_id'))})
        return initial


class VisualizationView(generic.ListView):
    template_name = "polls/viz_task.html"

    def get_queryset(self):
        return BoardTask.objects.filter().order_by("task_start_time")


