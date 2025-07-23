from rest_framework import serializers
from .article_serializer import ArticleSerializer

class ArticleListResponseSerializer(ArticleSerializer):
    """Serializer optimized for listing articles - only showing necessary information"""
    tag_list = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ['tag_list']

    def get_title(self, obj):
        """Get first 20 characters of title"""
        if obj.title and len(obj.title) > 20:
            return obj.title[:20] + "..."
        return obj.title

    def get_body(self, obj):
        """Get first 30 characters of body"""
        if obj.body and len(obj.body) > 30:
            return obj.body[:30] + "..."
        return obj.body

    def get_tag_list(self, obj):
        """Get list of tags as strings, limited to 3 tags"""
        tags = obj.tags.all()[:3]
        return [str(tag) for tag in tags]
