from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.translation import ugettext as _

from django.db.models import Count, Avg

# Bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource

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
        initial.update(some_object)
        initial.update({'task': Task.objects.get(pk=some_object.get('task_id'))})
        return initial


class VisualizationView(generic.ListView):
    template_name = "polls/viz_task.html"
    context_object_name = 'tasks_list'

    def get_queryset(self):
        return BoardTask.objects.all()

    def get(self, request, *args, **kwargs):

        # Data extract and transform
        tasks_set = BoardTask.objects.values("task_id__task_name")\
            .annotate(d_count=Count('task_id'), avg_rating=Avg('task_rating'))

        # inverse LD to DL
        v = {k: [dic[k] for dic in tasks_set] for k in tasks_set[0]}

        source = ColumnDataSource(data=v)

        print(v)

        p = figure(x_range=v['task_id__task_name'], plot_height=500, toolbar_location=None, title="Tasks Counts")

        p.vbar(x='task_id__task_name', top='d_count', width=0.9,
               source=source, line_color='white', color="#e84d60")

        p.xaxis.major_label_orientation = 1

        # Store components
        script, div = components(p)

        self.object_list = self.get_queryset()

        context = self.get_context_data(object_list=self.object_list, script=script, div=div)

        return self.render_to_response(context)





