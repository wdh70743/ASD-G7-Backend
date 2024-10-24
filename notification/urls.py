from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('update-preferences/', views.update_preferences, name='update_preferences'),
    path('get-preferences/', views.get_preferences, name='get_preferences'),
]