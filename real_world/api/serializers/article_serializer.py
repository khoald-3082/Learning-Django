from rest_framework import serializers
from django.utils.text import slugify
from ..models.article import Article

class ArticleSerializer(serializers.ModelSerializer):
    """Serializer optimized for base articles - only showing necessary information"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'author_name', 'created_at', 'comment_count', 'slug']
        read_only_fields = ['id', 'created_at', 'author_name', 'comment_count', 'slug']

    def get_comment_count(self, obj):
        """Get count of comments for the article"""
        return obj.comments.count()

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().update(instance, validated_data)
