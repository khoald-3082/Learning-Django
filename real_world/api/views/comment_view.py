from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from ..models import *
from ..serializers import *
from .helpers.custom_paginate import CustomPagination
from ..permissions.is_user import IsUserPermission
from ..common.constant import cache_time

# View for listing and creating comments for an article
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)
        return article.comments.all().order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsUserPermission()]
        return []

    def get_authenticators(self):
        if self.request.method == 'POST':
            return [JWTAuthentication()]
        return []

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)
        serializer.save(author=self.request.user, article=article)

# View for updating, and deleting a single comment
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserPermission]
    lookup_field = 'id'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)
        return article.comments.all()

    def get_object(self):
        obj = super().get_object()

        # Check if user can modify this comment
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.author != self.request.user:
                raise PermissionDenied("You don't have permission to modify this comment")

        return obj
