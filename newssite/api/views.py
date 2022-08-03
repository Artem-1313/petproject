from django.shortcuts import render
from rest_framework import generics
from newsapp.models import Article, Comment
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .serializers import ArticleSerializer, RetrieveSerialezer, CommentSerializer
# Create your views here.


class AllArticles(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'categories']
    search_fields = ['title']

class RetrieveArticle(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = RetrieveSerialezer

class NewsappAPI(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'categories']
    search_fields = ['title']


class CommentAPI(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        if self.request.user.is_authenticated:
            serializer.save(**{'author': self.request.user})
        else:
            print(serializer.save())



