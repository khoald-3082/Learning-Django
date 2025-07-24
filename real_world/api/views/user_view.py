from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models.user import User
from ..serializers.article_list_response_serializer import ArticleListResponseSerializer
from ..serializers.comment_serializer import CommentSerializer
from ..serializers.user_serializer import UserSerializer

"""Controller handle for API of User"""

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """GET user profile"""
    print(f"User: {request.user.is_authenticated}")  # Debug xem user là gì
    print(f"Is authenticated: {request.user.is_authenticated}")
    print(f"Auth header: {request.META.get('HTTP_AUTHORIZATION', 'None')}")
    user = request.user
    articles = user.articles.all().order_by('-created_at')
    comments = user.comments.all().order_by('-created_at')
    return Response({
        "profile": UserSerializer(user).data,
        "articles": ArticleListResponseSerializer(articles, many=True).data,
        "comments": CommentSerializer(comments, many=True).data
    })


@api_view(['POST'])
def register_user(request):
    """POST create user profile"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        try:
            serializer.save()
            return Response({'message': 'Register successful!'}, status=HTTPStatus.CREATED)
        except Exception as e:
            return Response({
                'error_message': str(e),
            }, status=HTTPStatus.BAD_REQUEST)

    else:
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
