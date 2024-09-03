from django.urls import path, include
from .views import CreateUserAPI, LoginAPI

urlpatterns = [
    path('create/', CreateUserAPI.as_view()),
    path('login/', LoginAPI.as_view()),
]
