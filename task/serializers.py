from rest_framework import serializers
from .models import Task, TaskFile, UserTask


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ['id', 'file_uri']  # Include necessary fields

class UserTaskSerializer(serializers.ModelSerializer):
    # assigned_by = serializers.StringRelatedField()  # Displaying the username or another string representation
    # assigned_to = serializers.StringRelatedField()  # Displaying the username or another string representation

    class Meta:
        model = UserTask
        fields = ['assigned_by', 'assigned_to']

class TaskSerializer(serializers.ModelSerializer):
    files = TaskFileSerializer(many=True, read_only=True)  # Related TaskFile instances
    users = UserTaskSerializer(source='user_tasks', many=True, read_only=True)  # Related UserTask instances

    class Meta:
        model = Task
        fields = '__all__'  # or explicitly list fields if needed
        read_only_fields = ('created_at', 'updated_at')
