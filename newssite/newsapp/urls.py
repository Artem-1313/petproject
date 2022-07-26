from django.urls import path, include
from .views import test, ListArticles, DetailArticle, LikeArticle, AddComment


urlpatterns = [

    path('', ListArticles.as_view(), name="main"),
    path('detail/<int:pk>/', DetailArticle.as_view(), name="article_detail"),
    path('article_like/<int:pk>/', LikeArticle.as_view(), name="article_like"),
    path('add_comment/<int:pk>/', AddComment.as_view(), name="comment_add"),
]
