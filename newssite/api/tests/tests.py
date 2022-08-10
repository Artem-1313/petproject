import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from newsapp.models import Article, Category, Comment
from django.contrib.auth import get_user_model
from api.serializers import ArticleSerializer, ArticleAll, RetrieveSerialezer, CategorySerializer
from rest_framework.authtoken.models import Token
from django.db.models import Q
# Create your tests here.
User = get_user_model()


class AllArticlesApiTestCase(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="testAPI")
        #  comment = Comment.objects.create(body="comment",article=self.article_3, author= self.user_1)
        self.user_1 = User.objects.create(email="artemthfc@gmail.com", first_name="Artem", last_name="khmil")
        self.article_1 = Article.objects.create(title="testAPI", body="test", author=self.user_1,
                                                categories=self.category, top_news=True)
        self.article_2 = Article.objects.create(title="test 2", body="test 2", author=self.user_1,
                                                categories=self.category)
        self.article_3 = Article.objects.create(title="test 21", body="test 21", author=self.user_1,
                                                categories=self.category)

        self.article_3.likes.add(self.user_1)

    def test_get_all_articles(self):
        url = reverse('all-articles')
        response = self.client.get(url)
        articles = Article.objects.all()
        serializer_data = ArticleAll(articles, many=True)
        self.assertEqual(response.data['results'], serializer_data.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_article(self):
        url = reverse('retrieve-article', kwargs={'pk': self.article_3.pk})
        response = self.client.get(url)
        article = Article.objects.get(pk=self.article_3.pk)
        serializer_data = RetrieveSerialezer(article)
        response.data['image'] = '/media/images/default.jpg'
        self.assertEqual(response.data, serializer_data.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_article_error(self):
        url = reverse('retrieve-article', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_categories(self):
        url = reverse('all-categories')
        response = self.client.get(url)
        categories = Category.objects.all()
        serializer_data = CategorySerializer(categories, many=True)
        self.assertEqual(response.data['results'], serializer_data.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_search_success(self):
        # url = ('/all/category/', {"search": self.category})
        url = '{url}?{filter}={value}'.format(url=reverse('all-categories'), filter='search', value=self.category)
        response = self.client.get(url)
        self.assertGreater(len(response.data['results']), 0)

    def test_category_search_error(self):
        # url = ('/all/category/', {"search": self.category})
        url = '{url}?{filter}={value}'.format(url=reverse('all-categories'), filter='search', value="blabla")
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 0)

    def test_top_news(self):
        """
        add comment filter
        """
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=2)
        url = reverse('top-news')
        response = self.client.get(url)
        id_top_like = [i.id for i in Article.objects.all() if i.likes.all().count() >= 1]
        articles = Article.objects.filter(( Q(pk__in=id_top_like) | Q(top_news=True)) &
                                          Q(created_article__range=(week_ago, today)))
        serializer_data = ArticleSerializer(articles, many=True)
        self.assertEqual(response.data['results'], serializer_data.data)