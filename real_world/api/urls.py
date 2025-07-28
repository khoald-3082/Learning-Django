from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import *

router = DefaultRouter()
app_name = 'api'

urlpatterns = [
    path('articles/', get_article, name='article-list'),
    path('articles/feed/', get_feed, name='article-feed'),
    path('articles/create/', create_article, name='article-create'),
    path('articles/<slug:slug>/', get_article, name='article-detail'),
    path('articles/<slug:slug>/update/', update_article, name='article-update'),
    path('articles/<slug:slug>/delete/', delete_article, name='article-delete'),
    path('articles/<slug:slug>/favorite/', add_favorite, name='article-favorite'),

    path('articles/<slug:slug>/comments/', comment_list, name='comment-list-create'),
    path('articles/<slug:slug>/comments/create/', create_comment, name='comment-create'),
    path('articles/<slug:slug>/comments/<int:id>/update/', update_comment, name='comment-update'),
    path('articles/<slug:slug>/comments/<int:id>/delete/', delete_comment, name='comment-delete'),

    path('tags/', TagView.as_view(), name='tag-list'),

    path('profiles/', get_profile, name='user-detail'),
    path('users/', register_user, name='user-register'),

    path('admin/profiles/', get_admin_profile, name='admin-user-detail'),

    path('', include(router.urls)),

    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
