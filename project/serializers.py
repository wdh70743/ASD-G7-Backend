from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        ref_name = 'ProjectAppUserSerializer'

class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    user_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True, source='users'
    )

    class Meta:
        model = Project
        fields = '__all__'
