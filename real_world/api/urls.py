from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ArticleView, CommentView, UserView, TagView

router = DefaultRouter()
app_name = 'api'

urlpatterns = [
    path('articles/', ArticleView.as_view(), name='article-list-create'),
    path('articles/<slug:slug>/', ArticleView.as_view(), name='article-detail-update-delete'),

    path('articles/<slug:slug>/comments/', CommentView.as_view(), name='comment-list-create'),
    path('articles/<slug:slug>/comments/<int:id>/', CommentView.as_view(), name='comment-update-delete'),

    path('tags/', TagView.as_view(), name='tag-list'),

    path('profiles/<str:username>/', UserView.as_view(), name='user-detail'),

    path('', include(router.urls)),
]
