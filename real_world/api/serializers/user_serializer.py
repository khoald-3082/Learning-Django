from rest_framework import serializers
from django.utils.text import slugify

from ..models.user import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer optimized for users - only showing necessary information"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'created_at', 'is_staff', 'password']
        read_only_fields = ['id', 'created_at', 'full_name']
        extra_kwargs = {'password': {'write_only': True}}
