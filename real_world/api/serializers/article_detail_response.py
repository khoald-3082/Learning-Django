from rest_framework import serializers
from .article_base_response import ArticleBaseResponseSerializer

class ArticleDetailResponseSerializer(ArticleBaseResponseSerializer):
    """Serializer optimized for detail view of an article - showing all information"""
    comments = serializers.SerializerMethodField()

    class Meta(ArticleBaseResponseSerializer.Meta):
        fields = ArticleBaseResponseSerializer.Meta.fields + ['comments']

    def get_comments(self, obj):
        """Get comments for the article"""
        all_comments = obj.comments.all()
        return [
            {
                "body": comment.body,
                "author": comment.author.username,
                "created_at": comment.created_at
            }
            for comment in all_comments
        ]
