from django.shortcuts import render
from rest_framework import generics, mixins, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Task, TaskFile, TaskComment, UserTask
from django.utils.decorators import method_decorator
from .serializers import TaskSerializer
from project.models import Project
from users.models import User


class CreateTaskAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @swagger_auto_schema(
        operation_description="Create a new task",
        responses={201: TaskSerializer()},
        tags=['Tasks'],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GetProjectTaskListAPI(generics.GenericAPIView):
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        operation_description="Get list of tasks for a specific project",
        manual_parameters=[
            openapi.Parameter('project_id', openapi.IN_PATH, description="Project ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: TaskSerializer(many=True), 400: "Bad Request"},
        tags=['Tasks'],
    )
    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')

        if not Project.objects.get(id=project_id):
            return Response({"error": "Project does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.filter(project__id=project_id)
        serializer = self.get_serializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserTaskListAPI(generics.GenericAPIView):
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        operation_description="Get list of tasks for a specific user",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: TaskSerializer(many=True), 400: "Bad Request"},
        tags=['Tasks'],
    )
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')

        if not User.objects.get(id=user_id):
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.filter(owner__id=user_id)
        serializer = self.get_serializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HandleArchiveTaskAPI(generics.GenericAPIView):
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        operation_description="Toggle archive status of a task",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['task_id'],
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            },
        ),
        responses={200: "Success message", 400: "Bad Request"},
        tags=['Tasks'],
    )
    def post(self, request, *args, **kwargs):
        task_id = request.data.get('task_id')

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        task.is_archived = not task.is_archived
        task.save()

        action = "archived" if task.is_archived else "unarchived"
        return Response({"message": f"Task has been {action} successfully."}, status=status.HTTP_200_OK)


class GetUserArchivedTaskListAPI(generics.GenericAPIView):
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        operation_description="Get list of archived tasks for a specific user",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: TaskSerializer(many=True), 400: "Bad Request"},
        tags=['Tasks'],
    )
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')

        if not User.objects.get(id=user_id):
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.filter(owner__id=user_id, is_archived=True)
        serializer = self.get_serializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUpdateDestroyTaskAPI(generics.GenericAPIView,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin
                                   ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a task",
        responses={200: TaskSerializer(), 404: "Not Found"},
        tags=['Tasks'],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a task",
        request_body=TaskSerializer,
        responses={200: TaskSerializer(), 400: "Bad Request", 404: "Not Found"},
        tags=['Tasks'],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a task",
        request_body=TaskSerializer,
        responses={200: TaskSerializer(), 400: "Bad Request", 404: "Not Found"},
        tags=['Tasks'],
    )
    def put(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a task",
        responses={204: "No Content", 404: "Not Found"},
        tags=['Tasks'],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class HandleTaskCommentAPI():
    pass


class HandleTaskFileAPI():
    pass


class HandleUserTaskAPI():
    pass
