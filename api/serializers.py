from rest_framework import serializers
from core.models import Task, Project, TimeEntry

from .exceptions import BadRequest


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'author']
        read_only_fields = ('id', 'author')

    def create(self, validated_data):
        instance = Project.objects.create(**validated_data, author=self.context['request'].user)
        return instance


class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = ['id', 'start', 'task', 'end']
        read_only_fields = ('id', 'start', 'end', 'task', 'end')


class TaskSerializer(serializers.ModelSerializer):
    time_entries = TimeEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Task
        # TODO: send also project_name (prefetch_related projects?)
        fields = ['id', 'name', 'project', 'author', 'time_entries']
        read_only_fields = ('id', 'author', 'time_entries')

    def create(self, validated_data):
        print(validated_data)
        current_task = Task.objects.filter(author=self.context['request'].user, time_entries__end__isnull=True).first()
        if current_task is None:
            instance = Task.objects.create(**validated_data, author=self.context['request'].user)
        else:
            raise BadRequest(detail='Already have running task')
        return instance

