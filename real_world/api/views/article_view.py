from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ..models.article import Article
from ..models.user import User
from ..serializers.article_detail_response_serializer import ArticleDetailResponseSerializer
from ..serializers.article_list_response_serializer import ArticleListResponseSerializer
from ..serializers.article_serializer import ArticleSerializer
from ..constants.enum import HTTPStatus

class ArticleView(APIView):
    """Controller handle for API of Articles"""

    def get(self, request, slug=None):
        if slug is not None:
            """GET detail by slug"""
            article = Article.objects.filter(slug=slug).first()
            if not article:
                return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)

            return Response(ArticleDetailResponseSerializer(article).data)
        else:
            """GET list of articles"""
            all_articles = Article.objects.all().order_by('-created_at')
            return Response({"data": ArticleListResponseSerializer(all_articles, many=True).data})

    def post(self, request):
        """POST create new article"""
        author = User.objects.filter(id=request.GET.get('user_id')).first()
        if not author:
            return Response({"error": "Author not found"}, status=404)

        article = ArticleSerializer(data=request.data)
        if article.is_valid():
            try:
                article.save(author=author)
                return Response(article.data, status=HTTPStatus.CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)

        return Response(article.errors, status=HTTPStatus.BAD_REQUEST)

    def put(self, request, slug=None):
        """PUT update article"""
        author = User.objects.filter(id=request.GET.get('user_id')).first()
        if not author:
            return Response({"error": "Unauthorized"}, status=HTTPStatus.UNAUTHORIZED)

        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)
        elif article.author != author:
            return Response({"error": "Forbidden"}, status=HTTPStatus.FORBIDDEN)

        article_serializer = ArticleSerializer(article, data=request.data, partial=True)
        if article_serializer.is_valid():
            try:
                article_serializer.update(article, article_serializer.validated_data)
                return Response(article_serializer.data, status=HTTPStatus.OK)
            except Exception as e:
                return Response({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)

        return Response(article.errors, status=HTTPStatus.BAD_REQUEST)

    def delete(self, request, slug=None):
        """DELETE article"""
        author = User.objects.filter(id=request.GET.get('user_id')).first()
        if not author:
            return Response({"error": "Unauthorized"}, status=HTTPStatus.UNAUTHORIZED)

        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)
        elif article.author != author:
            return Response({"error": "Forbidden"}, status=HTTPStatus.FORBIDDEN)

        article.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
