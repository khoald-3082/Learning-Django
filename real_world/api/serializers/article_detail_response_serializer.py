from rest_framework import serializers
from .article_serializer import ArticleSerializer

class ArticleDetailResponseSerializer(ArticleSerializer):
    """Serializer optimized for detail view of an article - showing all information"""
    tag_list = serializers.SerializerMethodField()
    favorites = serializers.SerializerMethodField()

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ['tag_list', 'favorites']


    def get_tag_list(self, obj):
        """Get list of tags as strings"""
        tags = obj.tags.all()
        return [str(tag) for tag in tags]

    def get_favorites(self, obj):
        """Get list of users who favorited the article"""
        favorites = obj.favorites.all()
        return [str(favorite.user.username) for favorite in favorites]
