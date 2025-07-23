from rest_framework import serializers
from ..models.article import Article

class ArticleBaseResponseSerializer(serializers.ModelSerializer):
    """Serializer optimized for base articles - only showing necessary information"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'author_name', 'tag_list', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_tag_list(self, obj):
        """Get list of tags as strings"""
        tags = obj.tags.all()
        return [str(tag) for tag in tags]
