from rest_framework import serializers
from django.utils.text import slugify
from ..models.comment import Comment

class CommentSerializer(serializers.ModelSerializer):
    """Serializer optimized for comments - only showing necessary information"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    article_slug = serializers.SlugField(source='article.slug', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author_name', 'created_at', 'article_slug']
        read_only_fields = ['id', 'created_at', 'author_name', 'article_slug']
