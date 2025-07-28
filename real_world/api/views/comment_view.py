from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models.article import Article
from ..models.user import User
from ..serializers.comment_serializer import CommentSerializer

@api_view(['GET'])
def comment_list(request, slug=None):
    """GET comments for article"""
    article = Article.objects.filter(slug=slug).first()
    if not article:
        return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)

    comments = article.comments.all().order_by('-created_at')
    return Response({"data": CommentSerializer(comments, many=True).data})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_comment(request, slug=None):
    """POST create comment for article"""
    author = request.user

    article = Article.objects.filter(slug=slug).first()
    if not article:
        return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)

    comment = CommentSerializer(data=request.data)
    if comment.is_valid():
        try:
            comment.save(author=author, article=article)
            return Response(comment.data, status=HTTPStatus.CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)

    return Response(article.errors, status=HTTPStatus.BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_comment(request, slug=None, id=None):
    """PUT update comment for article"""
    author = request.user

    article = Article.objects.filter(slug=slug).first()
    if not article:
        return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)

    comment = article.comments.filter(id=id).first()
    if not comment:
        return Response({"error": "Comment not found"}, status=HTTPStatus.NOT_FOUND)
    elif comment.author != author:
        return Response({"error": "Forbidden"}, status=HTTPStatus.FORBIDDEN)

    comment_serializer = CommentSerializer(comment, data=request.data, partial=True)
    if comment_serializer.is_valid():
        try:
            comment_serializer.update(comment, comment_serializer.validated_data)
            return Response(comment_serializer.data, status=HTTPStatus.OK)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)

    return Response(comment.errors, status=HTTPStatus.BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_comment(request, slug=None, id=None):
    """DELETE comment for article"""
    author = request.user

    article = Article.objects.filter(slug=slug).first()
    if not article:
        return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)
    elif article.author != author:
        return Response({"error": "Forbidden"}, status=HTTPStatus.FORBIDDEN)

    comment = article.comments.filter(id=id).first()
    if not comment:
        return Response({"error": "Comment not found"}, status=HTTPStatus.NOT_FOUND)
    elif comment.author != author:
        return Response({"error": "Forbidden"}, status=HTTPStatus.FORBIDDEN)

    comment.delete()
    return Response(status=HTTPStatus.NO_CONTENT)
