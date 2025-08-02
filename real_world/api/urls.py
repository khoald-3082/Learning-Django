from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import *

router = DefaultRouter()
app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),

    path('users/', RegisterUserView.as_view(), name='user-register'),
    path('profiles/', GetProfileView.as_view(), name='user-detail'),

    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('articles/', ArticleListCreateView.as_view(), name='article-list'),
    path('articles/feed/', ArticleFeedView.as_view(), name='article-feed'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/<slug:slug>/favorite/', FavoriteView.as_view(), name='article-favorite'),

    path('articles/<slug:slug>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('articles/<slug:slug>/comments/<int:id>/', CommentDetailView.as_view(), name='comment-update-delete'),

    path('follow/<str:username>/', FollowView.as_view(), name='follow-user'),

    path('tags/', TagListCreateView.as_view(), name='tag-list'),

    path('admin/profiles/', AdminProfileView.as_view(), name='admin-user-detail'),
]
