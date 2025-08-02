from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import *
from ..serializers import *
from ..permissions.is_user import IsUserPermission

# View for add and remove follow user
class FollowView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserPermission]

    def post(self, request, username=None):
        """POST add user to follow"""
        user_to_follow = get_object_or_404(User, username=username)
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        message = "User followed" if created else "User already followed"
        return Response(
            {"message": message},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, username=None):
        """DELETE remove follow user"""
        user_to_unfollow = get_object_or_404(User, username=username)
        follow = get_object_or_404(Follow, follower=request.user, following=user_to_unfollow)
        follow.delete()
        return Response(
            {"message": "User unfollowed"},
            status=status.HTTP_204_NO_CONTENT
        )
