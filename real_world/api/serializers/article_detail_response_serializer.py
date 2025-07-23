from rest_framework import serializers
from .article_serializer import ArticleSerializer

class ArticleDetailResponseSerializer(ArticleSerializer):
    """Serializer optimized for detail view of an article - showing all information"""
    tag_list = serializers.SerializerMethodField()

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ['tag_list']


    def get_tag_list(self, obj):
        """Get list of tags as strings"""
        tags = obj.tags.all()
        return [str(tag) for tag in tags]
