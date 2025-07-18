from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ArticleView, CommentView, UserView, TagView

router = DefaultRouter()
app_name = 'api'

urlpatterns = [
    path('articles/', ArticleView.as_view(), name='article-list-create'),
    path('articles/<int:id>/', ArticleView.as_view(), name='article-detail'),

    path('comments/', CommentView.as_view(), name='comment-create'),
    path('comments/<int:id>/', CommentView.as_view(), name='comment-delete'),

    path('tags/', TagView.as_view(), name='tag-list'),

    path('user/', UserView.as_view(), name='user-detail'),

    path('', include(router.urls)),
]
