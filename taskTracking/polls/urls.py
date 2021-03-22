from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view()),
    path('task/', views.TaskView.as_view(), name='task'),
    path('timetable/<int:pk>/', views.TaskModifyView.as_view(), name='task_modify'),
    path('timetable/', views.TimeTableView.as_view(), name='timetable'),
    path('viz/', views.VisualizationView.as_view(), name='viz')
]
