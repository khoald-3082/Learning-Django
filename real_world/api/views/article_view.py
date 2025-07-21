from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ..serializers.article_detail_response import ArticleDetailResponseSerializer
from ..models.article import Article
from ..models.user import User
from ..serializers.article_list_response import ArticleListResponseSerializer

class ArticleView(APIView):
    """Controller handle for API of Articles"""

    def get(self, request, id=None):
        if id is not None:
            """GET detail by id"""
            article = Article.objects.filter(id=id).first()
            if not article:
                raise NotFound("Article not found")

            return Response(ArticleDetailResponseSerializer(article).data)
        else:
            """GET list of articles"""
            all_articles = Article.objects.all().order_by('-created_at')
            return Response({"data": ArticleListResponseSerializer(all_articles, many=True).data})

    def post(self, request):
        """POST create new article"""
        return Response({"message": "Article created"})

    def put(self, request):
        """PUT update article"""
        return Response({"message": "Article updated"})

    def delete(self, request):
        """DELETE article"""
        return Response({"message": "Article deleted"})
