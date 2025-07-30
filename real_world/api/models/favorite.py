from django.db import models

from .article import Article
from .user import User

class Favorite(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=['user', 'article'],
                    name='unique_user_article_favorite'
                )
            ]
