from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


from .models import Task, TimeEntry


class TaskListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        try:
            active_time_entry = TimeEntry.objects.get(task__author=self.request.user, end__isnull=True)
        except TimeEntry.DoesNotExist:
            active_time_entry = None

        print(active_time_entry)

        return Task.objects.filter(author=self.request.user).prefetch_related('time_entries')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name']
    template_name = 'tasks/task_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name']


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


def finish_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.finish()

    return HttpResponseRedirect(reverse('task_detail', args=(task.id,)))


def restart_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.restart()

    return HttpResponseRedirect(reverse('task_detail', args=(task.id,)))
