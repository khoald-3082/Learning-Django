from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models.article import Article
from ..models.user import User
from ..serializers.comment_serializer import CommentSerializer

class CommentView(APIView):
    """Controller handle for API of Comments"""

    def get(self, request, slug=None):
        """GET comments for article"""
        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)

        comments = article.comments.all().order_by('-created_at')
        return Response({"data": CommentSerializer(comments, many=True).data})

    def post(self, request, slug=None):
        """POST create comment for article"""
        author = User.objects.filter(id=request.GET.get('user_id')).first()
        if not author:
            return Response({"error": "Author not found"}, status=HTTPStatus.UNAUTHORIZED)

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

    def put(self, request, slug=None, id=None):
        """PUT update comment for article"""
        author = User.objects.filter(id=request.GET.get('user_id')).first()
        if not author:
            return Response({"error": "Unauthorized"}, status=HTTPStatus.UNAUTHORIZED)

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

    def delete(self, request, slug=None, id=None):
        """DELETE comment for article"""
        author = User.objects.filter(id=request.GET.get('user_id')).first()
        if not author:
            return Response({"error": "Unauthorized"}, status=HTTPStatus.UNAUTHORIZED)

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
