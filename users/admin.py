from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'password', 'created_at')


# Register your models here.
admin.site.register(User, UserAdmin)
