from django.urls import path
from .views import CreateProjectAPI, RetrieveUpdateDestroyProjectAPI, ListProjectAPI, ListUserProjectsAPI

urlpatterns = [
    path('create/', CreateProjectAPI.as_view(), name='project-create'),
    path('<int:pk>/', RetrieveUpdateDestroyProjectAPI.as_view(), name='project-detail'),
    path('user/<int:user_id>/', ListUserProjectsAPI.as_view(), name='user-projects'),
    path('', ListProjectAPI.as_view(), name='project-list'),
]
