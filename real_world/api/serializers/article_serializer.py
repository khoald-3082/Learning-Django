from rest_framework import serializers
from django.utils.text import slugify
from ..models.article import Article
from ..models.tag import Tag

class ArticleSerializer(serializers.ModelSerializer):
    """Serializer optimized for base articles - only showing necessary information"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.SerializerMethodField()
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'author_name', 'created_at', 'comment_count', 'slug', 'tags']
        read_only_fields = ['id', 'created_at', 'author_name', 'comment_count', 'slug']

    def get_comment_count(self, obj):
        """Get count of comments for the article"""
        return obj.comments.count()

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        validated_data['slug'] = slugify(validated_data['title'])
        article = super().create(validated_data)
        self.create_tags(article, tags_data)
        return article

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        validated_data['slug'] = slugify(validated_data['title'])
        article = super().update(instance, validated_data)
        self.create_tags(article, tags_data)
        return article

    def create_tags(self, article, tags_data):
        for tag_name in tags_data:
            if tag_name and tag_name.strip():
                tag, created = Tag.objects.get_or_create(
                    name=tag_name.strip().lower()
                )
                article.tags.add(tag)
        delete_tags = article.tags.exclude(name__in=[tag.strip().lower() for tag in tags_data])
        if delete_tags.exists():
            article.tags.remove(*delete_tags)
