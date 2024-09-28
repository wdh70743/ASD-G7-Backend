from django.urls import path, include
from .views import CreateTaskAPI, GetProjectTaskListAPI, GetUserTaskListAPI, HandleArchiveTaskAPI, \
    GetUserArchivedTaskListAPI, RetrieveUpdateDestroyTaskAPI

urlpatterns = [
    path('create/', CreateTaskAPI.as_view(), name='create_task'),
    path('projects/<int:project_id>/tasks/', GetProjectTaskListAPI.as_view(), name='project_tasks'),
    path('users/<int:user_id>/tasks/', GetUserTaskListAPI.as_view(), name='user_tasks'),
    path('archive/', HandleArchiveTaskAPI.as_view(), name='archive_task'),
    path('users/<int:user_id>/tasks/archived/', GetUserArchivedTaskListAPI.as_view(), name='user_archived_tasks'),
    path('<int:pk>/', RetrieveUpdateDestroyTaskAPI.as_view(), name='task_detail'),
]
