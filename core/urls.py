from django.urls import path

from .views import TaskListView, TaskCreateView, TaskDetailView, finish_task, restart_task

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('tasks/new/', TaskCreateView.as_view(), name='task_new'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/finish/', finish_task, name='task_finish'),
    path('tasks/<int:pk>/restart/', restart_task, name='task_restart'),
]
