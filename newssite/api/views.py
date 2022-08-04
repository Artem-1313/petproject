from rest_framework.decorators import action
from django.db.models import Q
from django.db.models import Count
from newsapp.models import Article, Comment, Category
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ArticleSerializer, RetrieveSerialezer, CommentSerializer, CategorySerializer, UserSerializer
from django.contrib.auth import get_user_model
from .permissions import IsOwnerOrReadOnly, IsStaffUser, IsOwnerArticleOrReadOnly
import datetime

User = get_user_model()

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
    permission_classes = [IsAuthenticated & IsOwnerArticleOrReadOnly ]

   # @permission_classes([AllowAny])
    @action(methods=['post'], detail=True)
    def put_remove_like(self, request, pk=None):

        article = self.get_object()
        user = self.request.user
        if user in article.likes.all():
            article.likes.remove(user)
        else:
            article.likes.add(user)
        article.save()
        serializer = self.get_serializer(article)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(**{'author': self.request.user})


class CommentAPI(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(**{'author': self.request.user})


class CategoriesAPI(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']


class TopNews(ListAPIView):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=2)
    id_top_article = [i['article'] for i in list(Comment.objects.values('article').annotate(dcount=Count('article_id')))
                      if i['dcount'] >= 2]
    id_top_like = [i.id for i in Article.objects.all() if i.likes.all().count() >= 1]

    queryset = Article.objects.filter((Q(pk__in=id_top_article) | Q(pk__in=id_top_like) | Q(top_news=True)) &
                                      Q(created_article__range=(week_ago, today)))
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class UserAPI(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
