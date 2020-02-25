from django.db import models
from django.db.models.signals import post_save


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
        time_entry = TimeEntry(task=instance)
        time_entry.save()

    def __str__(self):
        return f'Task {self.name}'


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

    # TODO: add constraint for Task and only one TimeEntry with end=Null
