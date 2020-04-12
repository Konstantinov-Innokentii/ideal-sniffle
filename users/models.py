from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    @property
    def active_time_entry_data(self):
        TimeEntry = apps.get_model('core', 'TimeEntry')

        try:
            active_time_entry = TimeEntry.objects.get(task__author=self, end__isnull=True)
            active_time_entry = {'task': active_time_entry.task.name, 'start': int(active_time_entry.start.replace(tzinfo=timezone.utc).timestamp()), 'id': active_time_entry.task.pk}
        except TimeEntry.DoesNotExist:
            active_time_entry = None

        return active_time_entry
