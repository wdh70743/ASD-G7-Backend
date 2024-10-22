from rest_framework import serializers
from .models import Task, TaskFile, UserTask
from users.models import User
from project.models import Project
class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ['id', 'file_uri']  # Include necessary fields


class UserTaskSerializer(serializers.ModelSerializer):
    # assigned_by = serializers.StringRelatedField()  # Displaying the username or another string representation
    # assigned_to = serializers.StringRelatedField()  # Displaying the username or another string representation

    class Meta:
        model = UserTask
        fields = ['assigned_to']


class TaskSerializer(serializers.ModelSerializer):
    files = TaskFileSerializer(many=True, read_only=True)  # Related TaskFile instances
    users = UserTaskSerializer(source='user_tasks', many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'owner', 'priority', 'status', 'title', 'description', 'start_date', 'due_date', 'is_archived',
                  'archived_at', 'created_at', 'updated_at', 'files', 'users']

class TaskCreationSerializer(serializers.ModelSerializer):
    files = TaskFileSerializer(many=True, read_only=True)  # Related TaskFile instances
    uploaded_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    users = UserTaskSerializer(source='user_tasks', many=True, read_only=True)
    assigned_users = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False
    )
    owner = serializers.IntegerField(write_only=True)
    project = serializers.IntegerField(write_only=True)

    class Meta:
        model = Task
        fields = ['owner', 'project', 'priority', 'status', 'title', 'description', 'start_date', 'due_date', 'is_archived',
                  'archived_at', 'created_at', 'updated_at', 'files', 'uploaded_files', 'users', 'assigned_users']
    def create(self, validated_data):
        uploaded_files = validated_data.pop("uploaded_files", [])
        assigned_users = validated_data.pop('assigned_users', [])
        owner_id = validated_data.pop('owner')
        project_id = validated_data.pop('project')
        try:
            owner = User.objects.get(id=owner_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with id {owner_id} does not exist")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError(f"User with id {project_id} does not exist")

        task = Task.objects.create(owner=owner, project=project, **validated_data)



        for file in uploaded_files:
            TaskFile.objects.create(
                owner=task.owner,
                task=task,
                file_uri=file
            )

            # Create user assignments
        for user_id in assigned_users:
            try:
                assigned_user = User.objects.get(id=user_id)
                UserTask.objects.create(
                    task=task,
                    assigned_by=task.owner,
                    assigned_to=assigned_user  # Using the User instance instead of just the ID
                )
            except User.DoesNotExist:
                raise serializers.ValidationError(f"User with id {user_id} does not exist")

        return task
