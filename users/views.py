from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .serializers import UserSerializer
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class CreateUserAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Create a new user with email, username, and password",
        request_body=UserSerializer,
        responses={
            201: openapi.Response('User created successfully', UserSerializer),
            400: 'Bad Request: Invalid input or password missing'
        },
        tags=['Users'],
    )
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        # Encrypt the password
        if 'password' in data:
            data['password'] = make_password(data['password'])
        else:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Login with email and password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            }
        ),
        responses={
            200: 'Login successful',
            400: 'Bad Request: Missing email or password',
            401: 'Unauthorized: Invalid credentials'
        },
        tags=['Users'],
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if check_password(password, user.password):
            user_data = self.get_serializer(user).data
            return Response({'message': 'Login successful', 'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name='dispatch')
class RetrieveUpdateDestroyUserAPI(generics.GenericAPIView,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a specific user's details by their ID.",
        responses={200: UserSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific user's details using PUT. Full object replacement.",
        request_body=UserSerializer,
        responses={200: UserSerializer()}
    )
    def put(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific user's details using PATCH. Partial object update.",
        request_body=UserSerializer,
        responses={200: UserSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific user by their ID.",
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

