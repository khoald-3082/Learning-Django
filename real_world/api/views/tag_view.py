from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..common.constant import cache_time
from ..models import *
from ..serializers import *
from .helpers.custom_paginate import CustomPagination

# View for listing and creating tags
# @method_decorator(cache_page(cache_time["5m"]), name='get')
class TagListCreateView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Tag.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return []

    def get_authenticators(self):
        if self.request.method == 'POST':
            return [JWTAuthentication()]
        return []
