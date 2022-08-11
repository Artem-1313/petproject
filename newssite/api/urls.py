from rest_framework import routers
from django.urls import path, include
from .views import NewsappAPI, AllArticles, RetrieveArticle, CommentAPI, CategoriesAPI, TopNews, UserAPI, AddSubscriber
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('article', NewsappAPI, basename='articles')
router.register('comment', CommentAPI, basename='comments_api')
router.register('account', UserAPI, basename='account_api')

urlpatterns = [

    path('all/', AllArticles.as_view(), name="all-articles"),
    path('all/<int:pk>/', RetrieveArticle.as_view(), name="retrieve-article"),
    path('category/', CategoriesAPI.as_view(), name="all-categories"),
    path('topnews/', TopNews.as_view(), name="top-news"),
    path('add_subscriber/', AddSubscriber.as_view(), name="add-subscriber"),

]