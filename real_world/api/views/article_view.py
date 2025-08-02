from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from ..throttles.custom_view_throttle import CustomViewThrottle
from ..models import *
from ..serializers import *
from .helpers.custom_paginate import CustomPagination
from ..permissions.is_user import IsUserPermission
from ..common.constant import cache_time

# View for listing and creating articles
# @method_decorator(cache_page(cache_time["3m"]), name='get')
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
    def get_object(self):
        obj = super().get_object()

        # Check if user can modify this comment
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.author != self.request.user:
                raise PermissionDenied("You don't have permission to modify this article")

        return obj

# View for listing articles from followed authors
# @method_decorator(cache_page(cache_time["3m"]), name='get')
class ArticleFeedView(generics.ListAPIView):
    serializer_class = ArticleListResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_following_ids = Follow.objects.filter(
            follower=self.request.user
        ).values_list('following', flat=True)

        if not user_following_ids.exists():
            return Article.objects.none()

        return Article.objects.filter(
            author__in=user_following_ids
        ).order_by('-created_at')
