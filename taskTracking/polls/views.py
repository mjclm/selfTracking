from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.translation import ugettext as _

from django.db.models import F, ExpressionWrapper, fields
from django.db.models import Count, Sum, Avg

# Bokeh
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.layouts import row
from .bokehApps.bokeh_plot import bar_plot


from .models import BoardTask, Task
from .forms import TaskForm

from .utils import date_from_str_to_datetime, timedelta_to_seconds


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
        initial.update(some_object)
        initial.update({'task': Task.objects.get(pk=some_object.get('task_id'))})
        return initial


class VisualizationView(generic.ListView):
    template_name = "polls/viz_task.html"
    context_object_name = 'tasks_list'

    def get_queryset(self):
        return BoardTask.objects.all()

    def get(self, request, *args, **kwargs):

        # graph 1
        tasks_set = BoardTask.objects.values("task_id__task_name")\
            .annotate(d_count=Count('task_id'), avg_rating=Avg('task_rating'))
        v = {k: [dic[k] for dic in tasks_set] for k in tasks_set[0]}
        source1 = ColumnDataSource(data=v)

        p1 = figure(title="Average rating by task",
                    x_axis_label='task',
                    y_axis_label='Rating (1-10)', x_range=v['task_id__task_name'])

        p1.vbar(x='task_id__task_name', top='avg_rating', width=.9,
                line_color='white',
                color="#e84d60",
                legend_label="tasks", source=source1)

        p1.xaxis.major_label_orientation = 1

        # graph 2
        duration = ExpressionWrapper(
            (F("task_end_time") - F("task_start_time")) + (F("task_end_date") - F("task_start_date")),
            output_field=fields.DurationField())

        data = BoardTask.objects.annotate(duration=duration) \
            .values("task_id__task_name") \
            .annotate(sum_duration=Sum('duration')) \

        v = {k: [dic[k] for dic in data] for k in data[0]}

        # convert seconds to other unite
        v['sum_duration'] = [value.seconds / 60 for value in v['sum_duration']]

        source2 = ColumnDataSource(data=v)

        p2 = figure(title="Total time by task",
                    x_axis_label='task',
                    y_axis_label='Time (minutes)', x_range=v['task_id__task_name'])

        p2.vbar(x='task_id__task_name', top='sum_duration', width=.9,
                line_color='white',
                color="#e84d60",
                legend_label="tasks", source=source2)

        p2.xaxis.major_label_orientation = 1

        # Store components
        script, div = components(row(p1, p2))

        self.object_list = self.get_queryset()

        context = self.get_context_data(object_list=self.object_list, script=script, div=div)

        return self.render_to_response(context)





