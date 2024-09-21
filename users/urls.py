from django.urls import path, include
from .views import CreateUserAPI, LoginAPI, RetrieveUpdateDestroyUserAPI

urlpatterns = [
    path('create/', CreateUserAPI.as_view(), name='create_user'),
    path('<int:pk>/', RetrieveUpdateDestroyUserAPI.as_view(), name='retrieve_update_destroy_user'),
    path('login/', LoginAPI.as_view(), name='login_user'),
]
