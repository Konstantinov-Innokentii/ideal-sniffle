from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone


TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"


class Project(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="projects",
        null=False
    )

    def __str__(self):
        return f'Project {self.name}'


class Task(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True
    )
    author = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=False
    )

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return

        # TimeEntry.objects.filter(task=instance, end__isnull=True).update(end=timezone.now())

        # time_entry = TimeEntry(task=instance)
        # time_entry.save()

    def save(self, *args, **kwargs):

        if self.pk is None:
            TimeEntry.objects.filter(task__author=self.author, end__isnull=True).update(end=timezone.now())
            super().save(*args, **kwargs)
            time_entry = TimeEntry(task=self)
            time_entry.save()
        else:
            super().save(*args, **kwargs)


    @property
    def render_for_template(self):
        return f"{self.name}"

    @property
    def running(self):
        return self.time_entries.filter(end__isnull=True).exists()

    def restart(self):
        try:
            _ = TimeEntry.objects.get(task=self, end__isnull=True)
        except TimeEntry.DoesNotExist:
            new_time_entry = TimeEntry.objects.create(task=self)
            new_time_entry.save()

    def finish(self):
        current_time_entry = TimeEntry.objects.get(task=self, end__isnull=True)
        current_time_entry.end = timezone.now()
        current_time_entry.save()


post_save.connect(Task.post_create, sender=Task)


class TimeEntry(models.Model):
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="time_entries",
        null=False
    )

    start = models.DateTimeField(auto_now_add=True, blank=True)
    end = models.DateTimeField(null=True)

    @property
    def render_for_template(self):
        return f"{self.start.strftime(TIME_FORMAT)} - {self.end.strftime(TIME_FORMAT) if self.end else ''}"
