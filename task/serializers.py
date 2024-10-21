from rest_framework import serializers
from .models import Task, TaskFile


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# class TaskCommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaskComment
#         fields = '__all__'


class TaskFileSerializer(serializers.ModelSerializer):
    file_uri = serializers.FileField(required=True)
    class Meta:
        model = TaskFile
        fields = '__all__'
