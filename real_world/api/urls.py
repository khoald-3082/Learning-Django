from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import ArticleView, CommentView, TagView
from .views.user_view import get_profile, register_user

router = DefaultRouter()
app_name = 'api'

urlpatterns = [
    path('articles/', ArticleView.as_view(), name='article-list-create'),
    path('articles/<slug:slug>/', ArticleView.as_view(), name='article-detail-update-delete'),

    path('articles/<slug:slug>/comments/', CommentView.as_view(), name='comment-list-create'),
    path('articles/<slug:slug>/comments/<int:id>/', CommentView.as_view(), name='comment-update-delete'),

    path('tags/', TagView.as_view(), name='tag-list'),

    path('profiles/', get_profile, name='user-detail'),
    path('users/', register_user, name='user-register'),


    path('', include(router.urls)),

    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
