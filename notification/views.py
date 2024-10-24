from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from notification.models import Notification, NotificationPreference
from users.models import User
from rest_framework.response import Response

# --- List Notifications ---
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of notifications for a specific user.",
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="User ID"),
    ],
    responses={
        200: openapi.Response('List of notifications', openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Notification message'),
                    'type': openapi.Schema(type=openapi.TYPE_STRING, description='Notification type'),
                    'is_read': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Read status'),
                    'created_at': openapi.Schema(type=openapi.FORMAT_DATETIME, description='Creation time'),
                }
            )
        )),
        404: 'Not Found'
    },
    tags=['Notifications'],
)
@api_view(['GET'])
@csrf_exempt
def notification_list(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    notifications = Notification.objects.filter(recipient=user)
    response = [
        {
            'message': n.message,
            'type': n.notification_type,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat(),
        }
        for n in notifications
    ]
    return Response(response, status=200)

# --- Mark Notification as Read ---
@swagger_auto_schema(
    method='put',
    operation_description="Mark a specific notification as read.",
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="User ID"),
    ],
    responses={
        200: openapi.Response('Notification marked as read', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Response status'),
            }
        )),
        404: 'Notification not found'
    },
    tags=['Notifications'],
)
@api_view(['PUT'])
@csrf_exempt
def mark_notification_as_read(request, notification_id):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    try:
        user = User.objects.get(id=user_id)
        notification = Notification.objects.get(id=notification_id, recipient=user)
    except (User.DoesNotExist, Notification.DoesNotExist):
        return JsonResponse({'error': 'Notification or user not found'}, status=404)

    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'}, status=200)

# --- Update Notification Preferences ---
@swagger_auto_schema(
    method='post',
    operation_description="Update notification preferences for a specific user.",
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="User ID"),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'receive_task_updates': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Receive task updates'),
            'receive_project_updates': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Receive project updates'),
            'receive_reminders': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Receive reminders'),
            'custom_reminder_interval': openapi.Schema(type=openapi.TYPE_INTEGER, description='Custom reminder interval in hours')
        },
        required=['receive_task_updates', 'receive_project_updates', 'receive_reminders']
    ),
    responses={
        200: openapi.Response('Preferences updated', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Response status'),
            }
        )),
    },
    tags=['Notifications'],
)
@api_view(['POST'])
@csrf_exempt
def update_preferences(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    try:
        user = User.objects.get(id=user_id)
        user_pref, created = NotificationPreference.objects.get_or_create(user=user)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    user_pref.receive_task_updates = request.data.get('receive_task_updates', user_pref.receive_task_updates)
    user_pref.receive_project_updates = request.data.get('receive_project_updates', user_pref.receive_project_updates)
    user_pref.receive_reminders = request.data.get('receive_reminders', user_pref.receive_reminders)
    user_pref.custom_reminder_interval = request.data.get('custom_reminder_interval', user_pref.custom_reminder_interval)
    user_pref.save()

    return JsonResponse({'status': 'success'}, status=200)


@swagger_auto_schema(
    method='get',
    operation_description="Retrieve notification preferences for a specific user.",
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="User ID"),
    ],
    responses={
        200: openapi.Response('User notification preferences', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'receive_task_updates': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Receive task updates'),
                'receive_project_updates': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                          description='Receive project updates'),
                'receive_reminders': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Receive reminders'),
                'custom_reminder_interval': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                           description='Custom reminder interval in hours'),
            }
        )),
        404: 'User or preferences not found'
    },
    tags=['Notifications'],
)
@api_view(['GET'])
@csrf_exempt
def get_preferences(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    try:
        user = User.objects.get(id=user_id)
        preferences = NotificationPreference.objects.get(user=user)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except NotificationPreference.DoesNotExist:
        return JsonResponse({'error': 'Notification preferences not found'}, status=404)

    response_data = {
        'receive_task_updates': preferences.receive_task_updates,
        'receive_project_updates': preferences.receive_project_updates,
        'receive_reminders': preferences.receive_reminders,
        'custom_reminder_interval': preferences.custom_reminder_interval
    }
    return JsonResponse(response_data, status=200)
