from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page

from ..throttles.custom_view_throttle import CustomViewThrottle
from ..models import *
from ..serializers import *
from .helpers.custom_paginate import CustomPagination
from ..permissions.is_user import IsUserPermission

# View for listing and creating articles
class ArticleListCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleListResponseSerializer
    throttle_classes = [CustomViewThrottle]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-created_at')

        # Filter by tag
        filter_tag = self.request.query_params.get('tag', None)
        if filter_tag:
            queryset = queryset.filter(tags__name__iexact=filter_tag.strip())

        # Filter by author
        filter_author = self.request.query_params.get('author', None)
        if filter_author:
            queryset = queryset.filter(author__username=filter_author.strip())

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleSerializer
        return ArticleListResponseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsUserPermission()]
        return []

    def get_authenticators(self):
        if self.request.method == 'POST':
            return [JWTAuthentication()]
        return []

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# View for detail, updating, and deleting a single article
class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArticleDetailResponseSerializer
        return ArticleSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated()]

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return [JWTAuthentication(), IsUserPermission()]

    def perform_update(self, serializer):
        article = self.get_object()
        if article.author != self.request.user:
            raise PermissionDenied("You don't have permission to edit this article")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You don't have permission to delete this article")
        instance.delete()

# View for listing articles from followed authors
# @cache_page(60 * 1)
class ArticleFeedView(generics.ListAPIView):
    serializer_class = ArticleListResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        # products = cache.get(cache_key)
        user_following_ids = Follow.objects.filter(
            follower=self.request.user
        ).values_list('following', flat=True)

        if not user_following_ids.exists():
            return Article.objects.none()

        return Article.objects.filter(
            author__in=user_following_ids
        ).order_by('-created_at')
