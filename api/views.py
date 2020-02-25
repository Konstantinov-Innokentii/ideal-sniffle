from django.utils import timezone

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from core.models import Task, Project, TimeEntry
from .serializers import TaskSerializer, ProjectSerializer, TimeEntrySerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(author=self.request.user)
        return queryset

    # TODO: detailed error codes

    @action(detail=True, methods=['put'])
    def stop(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            current_time_entry = TimeEntry.objects.get(task=task, end__isnull=True)
            current_time_entry.end = timezone.now()
            current_time_entry.save()
            response = Response(status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
        except TimeEntry.DoesNotExist:
            response = Response(status=status.HTTP_400_BAD_REQUEST)

        return response

    @action(detail=True, methods=['put'])
    def rerun(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            _ = TimeEntry.objects.get(task=task, end__isnull=True)
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
        except TimeEntry.DoesNotExist:
            new_time_entry = TimeEntry.objects.create(task=task)
            new_time_entry.save()
            response = Response(status=status.HTTP_200_OK)
        return response


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.filter(author=self.request.user)
        return queryset



# class TimeEntryViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = TimeEntry.objects.all()
#     serializer_class = TimeEntry
#
