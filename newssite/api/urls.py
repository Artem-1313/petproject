from rest_framework import routers
from django.urls import path, include
from .views import NewsappAPI, AllArticles, RetrieveArticle, CommentAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('article', NewsappAPI, basename='articles')
router.register('comment', CommentAPI, basename='comments_api')

urlpatterns = [

    path('all/', AllArticles.as_view()),
    path('all/<int:pk>/', RetrieveArticle.as_view()),



]