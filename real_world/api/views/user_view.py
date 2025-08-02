from http import HTTPStatus
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import *
from ..permissions.is_user import IsUserPermission

# View for getting user profile and articles/comments
class GetProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserPermission]

    def get(self, request):
        user = request.user
        articles = user.articles.all().order_by('-created_at')[:3]
        comments = user.comments.all().order_by('-created_at')[:3]
        return Response({
            "profile": UserSerializer(user).data,
            "articles": ArticleListResponseSerializer(articles, many=True).data,
            "comments": CommentSerializer(comments, many=True).data
        })


# View for user registration
class RegisterUserView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                serializer.save()
                return Response({'message': 'Register successful!'}, status=HTTPStatus.CREATED)
            except Exception as e:
                return Response({
                    'error_message': str(e),
                }, status=HTTPStatus.BAD_REQUEST)
        else:
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
