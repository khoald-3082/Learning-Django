from rest_framework import serializers
from django.utils.text import slugify
from ..models.tag import Tag

class TagSerializer(serializers.ModelSerializer):
    """Serializer optimized for tags - only showing necessary information"""
    article_count = serializers.IntegerField(source='articles.count', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'article_count']
        read_only_fields = ['id', 'article_count']
