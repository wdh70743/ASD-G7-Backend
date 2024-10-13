from django.shortcuts import render
from rest_framework import generics, mixins, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Task, TaskFile, TaskComment, UserTask
from django.utils.decorators import method_decorator
from .serializers import TaskSerializer, TaskCommentSerializer, TaskFileSerializer
from project.models import Project
from users.models import User
from django.db import transaction


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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


# Create Comment
# Get Comment List
# Delete Comment List
# Edit Comment List
@method_decorator(csrf_exempt, name='dispatch')
class CreateCommentAndGetCommentListAPI(generics.GenericAPIView):
    serializer_class = TaskCommentSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user making the comment'),
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the task to comment on'),
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='The comment text'),
            },
            required=['user_id', 'task_id', 'comment'],
        ),
        responses={
            200: openapi.Response('Comment saved successfully', TaskCommentSerializer),
            404: openapi.Response('Error', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            })),
        },
        tags=['Tasks'],
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        task_id = kwargs.get('task_id')
        comment = request.data.get('comment', None)

        if not user_id or not task_id or not comment:
            return Response({'error': 'user_id, task_id and comment must be provided'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        task_comment = TaskComment.objects.create(owner=user, task=task, comment=comment)
        task_comment = self.get_serializer(task_comment)
        return Response({'message': 'comment saved successfully', 'response': task_comment.data},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of comments', TaskCommentSerializer(many=True)),
            404: openapi.Response('Error', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            })),
        },
        tags=['Tasks'],
    )
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        task_comments = TaskComment.objects.filter(task=task)
        task_comments_serialised = self.get_serializer(task_comments, many=True)
        return Response(task_comments_serialised.data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class DeleteAndUpdateCommentAPI(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = TaskCommentSerializer
    queryset = TaskComment.objects.all()
    lookup_field = 'comment_id'

    @swagger_auto_schema(
        request_body=TaskCommentSerializer,
        responses={
            200: openapi.Response('Comment updated successfully', TaskCommentSerializer),
            404: openapi.Response('Error', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            })),
        },
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=TaskCommentSerializer,
        responses={
            200: openapi.Response('Comment updated successfully', TaskCommentSerializer),
            404: openapi.Response('Error', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            })),
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: 'Comment deleted successfully',
            404: openapi.Response('Error', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            })),
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Delete File
# Update File
@method_decorator(csrf_exempt, name='dispatch')
class CreateFileAndGetFileListAPI(generics.GenericAPIView):
    serializer_class = TaskFileSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user uploading the file'),
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                          description='ID of the task associated with the file'),
                'file_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the file'),
                'file_uri': openapi.Schema(type=openapi.TYPE_FILE, description='File to upload'),
            },
            required=['user_id', 'task_id', 'file_name', 'file_uri']  # Make sure to specify required fields
        ),
        responses={
            201: openapi.Response('File uploaded successfully', TaskFileSerializer),
            400: 'Invalid request',
            404: 'User or Task not found',
        },
        operation_description="Upload a file associated with a specific task and user."
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        task_id = kwargs.get('task_id')
        file_name = request.data.get('file_name', None)
        file_uri = request.data.get('file_uri', None)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        task_file = TaskFile.objects.create(owner=user, task=task, file_name=file_name, file_uri=file_uri)
        task_file = self.get_serializer(task_file)
        return Response({'message': 'File uploaded successfully', 'response': task_file.data},
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of files associated with the task', TaskFileSerializer(many=True)),
            404: 'Task not found',
        },
        operation_description="Retrieve a list of files associated with a specific task."
    )
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        task_files = TaskFile.objects.filter(task=task)
        serialized_files = self.get_serializer(task_files, many=True)
        return Response(serialized_files.data, status=status.HTTP_200_OK)
@method_decorator(csrf_exempt, name='dispatch')
class DeleteAndUpdateFileAPI(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = TaskFileSerializer
    queryset = TaskFile.objects.all()

    @swagger_auto_schema(
        request_body=TaskFileSerializer,
        responses={
            200: openapi.Response('File updated successfully', TaskFileSerializer),
            404: openapi.Response('Error', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            })),
        },
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=TaskFileSerializer,
        responses={
            200: openapi.Response('File updated successfully', TaskFileSerializer),
            404: openapi.Response('Error', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            })),
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: 'File deleted successfully',
            404: openapi.Response('Error', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            })),
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class AssignTaskToUserAPI(generics.GenericAPIView):
    @swagger_auto_schema(
        operation_description="Assign users to a task.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'assigned_by': openapi.Schema(type=openapi.TYPE_INTEGER,
                                              description='ID of the user who assigns the task'),
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the task'),
                'user_ids': openapi.Schema(type=openapi.TYPE_ARRAY,
                                           items=openapi.Items(type=openapi.TYPE_INTEGER),
                                           description='List of user IDs to assign')
            },
            required=['task_id', 'user_ids', 'assigned_by']
        ),
        responses={
            200: openapi.Response('Success', openapi.Schema(type=openapi.TYPE_OBJECT,
                                                            properties={
                                                                'message': openapi.Schema(type=openapi.TYPE_STRING)
                                                            }
                                                            )),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT,
                                                                properties={
                                                                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                                                                }
                                                                )),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT,
                                                              properties={
                                                                  'error': openapi.Schema(type=openapi.TYPE_STRING)
                                                              }
                                                              )),
        }, tags=['Tasks'],

    )
    def post(self, request, *args, **kwargs):
        assigned_by = request.data.get('assigned_by', None)
        task_id = request.data.get('task_id', None)
        user_ids = request.data.get('user_ids', None)

        if not task_id or not user_ids and not assigned_by:
            return Response({'error': 'task_id, user_ids and assigned_by must be provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            assigned_by = User.objects.get(id=assigned_by)
        except User.DoesNotExist:
            return Response({'error': 'User who wants to assign not found'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            for user_id in user_ids:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({'error': f'User with ID {user_id} not found'}, status=status.HTTP_404_NOT_FOUND)

                if UserTask.objects.filter(task=task, assigned_to=user).exists():
                    return Response({'error': f'User with ID {user_id} is already assigned to the task'},
                                    status=status.HTTP_400_BAD_REQUEST)

                UserTask.objects.create(task=task, assigned_to=user, assigned_by=assigned_by)

        return Response({'message': 'Users assigned to the task successfully'}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateAssignedUsersAPI(generics.GenericAPIView):

    @swagger_auto_schema(
        operation_description="Update users assigned to a task.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'assigned_by': openapi.Schema(type=openapi.TYPE_INTEGER,
                                              description='ID of the user who assigns the task'),
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the task'),
                'user_ids': openapi.Schema(type=openapi.TYPE_ARRAY,
                                           items=openapi.Items(type=openapi.TYPE_INTEGER),
                                           description='List of user IDs to update (remove if not present)')
            },
            required=['task_id', 'user_ids', 'assigned_by']
        ),
        responses={
            200: openapi.Response('Success', openapi.Schema(type=openapi.TYPE_OBJECT,
                                                            properties={
                                                                'message': openapi.Schema(type=openapi.TYPE_STRING)
                                                            }
                                                            )),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT,
                                                                properties={
                                                                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                                                                }
                                                                )),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT,
                                                              properties={
                                                                  'error': openapi.Schema(type=openapi.TYPE_STRING)
                                                              }
                                                              )),
        },
        tags=['Tasks'],
    )
    def post(self, request, *args, **kwargs):
        assigned_by = request.data.get('assigned_by', None)
        task_id = request.data.get('task_id', None)
        user_ids = request.data.get('user_ids', None)

        if not task_id or not user_ids or not assigned_by:
            return Response({'error': 'task_id, user_ids and assigned_by must be provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            assigned_by = User.objects.get(id=assigned_by)
        except User.DoesNotExist:
            return Response({'error': 'User who wants to assign not found'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            assigned_users = UserTask.objects.filter(task=task)
            assigned_user_ids = set(assigned_users.values_list('assigned_to_id', flat=True))

            users_to_remove = assigned_user_ids - set(user_ids)

            for user_id in users_to_remove:
                UserTask.objects.filter(task=task, assigned_to_id=user_id).delete()

            users_to_add = set(user_ids) - assigned_user_ids

            for user_id in users_to_add:
                try:
                    user = User.objects.get(id=user_id)
                    UserTask.objects.create(task=task, assigned_by=assigned_by, assigned_to=user)
                except User.DoesNotExist:
                    return Response({'error': f'User with ID {user_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Users assigned to the task updated successfully'}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class GetAssignedTaskListFromProjectAPI(generics.GenericAPIView):
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of tasks assigned to a user within a specific project.",
        manual_parameters=[
            openapi.Parameter('project_id', openapi.IN_PATH, description="ID of the project",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('user_id', openapi.IN_PATH, description="ID of the user", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(
                'Success',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'assigned_tasks': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT),
                            description="List of assigned tasks",
                        )
                    },
                )
            ),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)})),
        },
        tags=['Tasks'],
    )
    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        user_id = kwargs.get('user_id')

        if not project_id or not user_id:
            return Response({'error': 'project_id and user_id must be provided'})

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        assigned_tasks = Task.objects.filter(project=project, user_tasks__assigned_to=user).distinct()
        serializer = self.serializer_class(assigned_tasks, many=True)
        return Response({'assigned_tasks': serializer.data}, status=status.HTTP_200_OK)
