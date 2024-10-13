from django.urls import path
from .views import CreateProjectAPI, RetrieveUpdateDestroyProjectAPI, ListProjectAPI, ListUserProjectsAPI, \
    SearchUserInProjectAPI

urlpatterns = [
    path('create/', CreateProjectAPI.as_view(), name='project-create'),
    path('<int:pk>/', RetrieveUpdateDestroyProjectAPI.as_view(), name='project-detail'),
    path('user/<int:user_id>/', ListUserProjectsAPI.as_view(), name='user-projects'),
    path('', ListProjectAPI.as_view(), name='project-list'),
    path('<int:project_id>/search/', SearchUserInProjectAPI.as_view(), name='project-user-search'),
]
