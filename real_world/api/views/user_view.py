from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models.user import User
from ..serializers.article_list_response_serializer import ArticleListResponseSerializer
from ..serializers.comment_serializer import CommentSerializer
from ..serializers.user_serializer import UserSerializer

class UserView(APIView):
    """Controller handle for API of User"""

    def get(self, request, username=None):
        """GET user profile"""
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error": "Unauthorized"}, status=HTTPStatus.NOT_FOUND)
        articles = user.articles.all().order_by('-created_at')
        comments = user.comments.all().order_by('-created_at')
        return Response({
            "profile": UserSerializer(user).data,
            "articles": ArticleListResponseSerializer(articles, many=True).data,
            "comments": CommentSerializer(comments, many=True).data
        })


    def post(self, request):
        """POST create user profile"""
        return Response({"message": "User profile created"})
