from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

from .helpers.paginate_helper import paginate_queryset

from ..models.favorite import Favorite
from ..models.article import Article
from ..models.follow import Follow
from ..serializers.article_detail_response_serializer import ArticleDetailResponseSerializer
from ..serializers.article_list_response_serializer import ArticleListResponseSerializer
from ..serializers.article_serializer import ArticleSerializer

@api_view(['GET'])
def get_article(request, slug=None):
    if slug is not None:
        """GET detail by slug"""
        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)

        return Response(ArticleDetailResponseSerializer(article).data)
    else:
        """GET list of articles"""
        all_articles = Article.objects.all().order_by('-created_at')
        filter_tag = request.query_params.get('tag', None)
        if filter_tag:
            all_articles = all_articles.filter(tags__name__iexact=filter_tag.strip())
        filter_author = request.query_params.get('author', None)
        if filter_author:
            all_articles = all_articles.filter(author__username=filter_author.strip())

        return paginate_queryset(all_articles, request, ArticleListResponseSerializer)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_article(request):
    """POST create new article"""
    author = request.user

    article = ArticleSerializer(data=request.data)
    if article.is_valid():
        try:
            article.save(author=author)
            return Response(article.data, status=HTTPStatus.CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)

    return Response(article.errors, status=HTTPStatus.BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_article(request, slug=None):
    """PUT update article"""
    author = request.user

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

    return Response(article_serializer.errors, status=HTTPStatus.BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_article(request, slug=None):
    """DELETE article"""
    author = request.user

    article = Article.objects.filter(slug=slug).first()
    if not article:
        return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)
    elif article.author != author:
        return Response({"error": "Forbidden"}, status=HTTPStatus.FORBIDDEN)

    article.delete()
    return Response(status=HTTPStatus.NO_CONTENT)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_feed(request, slug=None):
    """GET list of followed articles"""
    user_following_ids = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    if not user_following_ids.exists():
        return Response({"data": []})

    all_articles = Article.objects.filter(author__in=user_following_ids).order_by('-created_at')
    return Response({"data": ArticleListResponseSerializer(all_articles, many=True).data})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_favorite(request, slug=None):
    """POST add article to favorites"""
    article = Article.objects.filter(slug=slug).first()
    if not article:
        return Response({"error": "Article not found"}, status=HTTPStatus.NOT_FOUND)

    try:
        Favorite.objects.get_or_create(user=request.user, article=article)
        return Response({"message": "Article added to favorites"}, status=HTTPStatus.CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)
