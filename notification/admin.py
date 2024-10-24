from django.contrib import admin
from .models import Notification, NotificationPreference

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'message', 'notification_type')
    readonly_fields = ('created_at',)

class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'receive_task_updates', 'receive_project_updates', 'receive_reminders', 'custom_reminder_interval')
    list_filter = ('receive_task_updates', 'receive_project_updates', 'receive_reminders')
    search_fields = ('user__username',)

# Register the models with the admin site
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationPreference, NotificationPreferenceAdmin)
