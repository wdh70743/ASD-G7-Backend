from django.urls import path, include
from .views import CreateTaskAPI, GetProjectTaskListAPI, GetUserTaskListAPI, HandleArchiveTaskAPI, \
    GetUserArchivedTaskListAPI, RetrieveUpdateDestroyTaskAPI, AssignTaskToUserAPI, UpdateAssignedUsersAPI, \
    GetAssignedTaskListFromProjectAPI, CreateCommentAndGetCommentListAPI, DeleteAndUpdateCommentAPI, \
    CreateFileAndGetFileListAPI, DeleteAndUpdateFileAPI

urlpatterns = [
    path('create/', CreateTaskAPI.as_view(), name='create_task'),
    path('projects/<int:project_id>/tasks/', GetProjectTaskListAPI.as_view(), name='project_tasks'),
    path('users/<int:user_id>/tasks/', GetUserTaskListAPI.as_view(), name='user_tasks'),
    path('archive/', HandleArchiveTaskAPI.as_view(), name='archive_task'),
    path('users/<int:user_id>/tasks/archived/', GetUserArchivedTaskListAPI.as_view(), name='user_archived_tasks'),
    path('<int:pk>/', RetrieveUpdateDestroyTaskAPI.as_view(), name='task_detail'),
    path('assign/', AssignTaskToUserAPI.as_view(), name='assign-task'),
    path('update-assigned-users/', UpdateAssignedUsersAPI.as_view(), name='update-assigned-users'),
    path('projects/<int:project_id>/users/<int:user_id>/assigned/',
         GetAssignedTaskListFromProjectAPI.as_view(), name='get-assigned-tasks'),
    path('<int:task_id>/comments/', CreateCommentAndGetCommentListAPI.as_view(), name='create-get-comments'),
    path('comments/<int:comment_id>/', DeleteAndUpdateCommentAPI.as_view(), name='comments-details'),
    path('<int:task_id>/files/', CreateFileAndGetFileListAPI.as_view(), name='create-get-files'),
    path('files/<int:file_id>/', DeleteAndUpdateFileAPI.as_view(), name='files-details'),

]
