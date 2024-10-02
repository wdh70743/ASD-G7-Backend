from django.shortcuts import render
from users.models import User
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Project
from .serializers import ProjectSerializer

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class CreateProjectAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    API view to create a new project.
    """
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    queryset = Project.objects.all()

    @swagger_auto_schema(
        operation_description="Create a new project. Specify project name, description, start date, end date, priority (low, medium, high), and status (true or false). Additionally, provide a list of user IDs to associate with the project.",
        request_body=ProjectSerializer,
        responses={
            201: openapi.Response('Project created successfully', ProjectSerializer),
            400: 'Bad Request: Invalid input'
        },
        tags=['Projects'],
    )
    def post(self, request, *args, **kwargs):
        user_ids = request.data.get('user_ids', [])
        owner_id = request.data.get('owner')

        try:
            owner = User.objects.get(id=owner_id)
        except User.DoesNotExist:
            return Response({"error": "Owner ID is invalid."}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(id__in=user_ids)
        if len(users) != len(user_ids):
            return Response({"error": "One or more user IDs are invalid"}, status=status.HTTP_400_BAD_REQUEST)

        request_data = request.data.copy()
        request_data['owner'] = owner.id

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(owner = owner)
            project.users.set(users)
            project.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class ListProjectAPI(generics.GenericAPIView, mixins.ListModelMixin):
    """
    API view to list all projects.
    """
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    queryset = Project.objects.all()

    @swagger_auto_schema(
        operation_description="Retrieve a list of all projects, showing details such as project name, description, start date, end date, priority, and status.",
        responses={200: ProjectSerializer(many=True)},
        tags=['Projects'],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class RetrieveUpdateDestroyProjectAPI(generics.GenericAPIView,
                                      mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.DestroyModelMixin):
    """
    API view to retrieve, update, or delete a specific project by its ID.
    """
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    @swagger_auto_schema(
        operation_description="Retrieve a specific project by its ID.",
        responses={200: ProjectSerializer()},
        tags=['Projects'],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific project using PUT. Specify the project name, description, start date, end date, priority (low, medium, high), and status. Optionally, update the list of user IDs.",
        request_body=ProjectSerializer,
        responses={200: ProjectSerializer()},
        tags=['Projects'],
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        user_ids = request.data.get('user_ids', [])
        users = User.objects.filter(id__in=user_ids)

        if len(users) != len(user_ids):
            return Response({"error": "One or more user IDs are invalid"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            project = serializer.save()
            project.users.set(users)
            project.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific project by its ID.",
        responses={204: "No Content"},
        tags=['Projects'],
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class ListUserProjectsAPI(generics.GenericAPIView, mixins.ListModelMixin):
    """
    API view to list all projects associated with a specific user.
    """
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Project.objects.filter(users__id=user_id)  # Filter projects by user ID

    @swagger_auto_schema(
        operation_description="Retrieve a list of all projects for a specific user.",
        responses={200: ProjectSerializer(many=True)},
        tags=['Projects'],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)