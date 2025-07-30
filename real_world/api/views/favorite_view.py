from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import *
from ..serializers import *
from ..permissions.is_user import IsUserPermission

# View for adding and removing articles from favorites
class FavoriteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserPermission]

    def post(self, request, slug=None):
        """POST add article to favorites"""
        article = get_object_or_404(Article, slug=slug)

        try:
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                article=article
            )
            message = "Article added to favorites" if created else "Article already in favorites"
            return Response(
                {"message": message},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_BAD_REQUEST
            )

    def delete(self, request, slug=None):
        """DELETE remove article from favorites"""
        article = get_object_or_404(Article, slug=slug)

        try:
            favorite = Favorite.objects.get(user=request.user, article=article)
            favorite.delete()
            return Response(
                {"message": "Article removed from favorites"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Favorite.DoesNotExist:
            return Response(
                {"error": "Article not in favorites"},
                status=status.HTTP_404_NOT_FOUND
            )
