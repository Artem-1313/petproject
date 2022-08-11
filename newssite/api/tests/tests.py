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
        self.user_2 = User.objects.create(email="joe@gmail.com", first_name="Joe", last_name="Tribbiani")
        self.user_2.set_password('131313!')
        self.user_2.save()
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

    def test_article_filter_by_user(self):
        url = '{url}?{filter}={value}'.format(url=reverse('all-articles'), filter='author', value=self.user_1.id)
        response = self.client.get(url)
        self.assertGreater(len(response.data['results']), 0)

    def test_article_filter_by_user_error(self):
        url = '{url}?{filter}={value}'.format(url=reverse('all-articles'), filter='author', value=self.user_2.id)
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 0)


    def test_get_all_categories(self):
        url = reverse('all-categories')
        response = self.client.get(url)
        categories = Category.objects.all()
        serializer_data = CategorySerializer(categories, many=True)
        self.assertEqual(response.data['results'], serializer_data.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_search_success(self):
        url = '{url}?{filter}={value}'.format(url=reverse('all-categories'), filter='search', value=self.category)
        response = self.client.get(url)
        self.assertGreater(len(response.data['results']), 0)

    def test_category_search_error(self):
        # url = ('/all/category/', {"search": self.category})
        url = '{url}?{filter}={value}'.format(url=reverse('all-categories'), filter='search', value="blabla")
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 0)

    def test_category_filter_success(self):
        url = f"/api/category/?name={self.category}"
        response = self.client.get(url)
        self.assertGreater(len(response.data['results']), 0)

    def test_category_filter_error(self):
        url = f"/api/category/?name=kkkkkkk"
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
        articles = Article.objects.filter((Q(pk__in=id_top_like) | Q(top_news=True)) &
                                          Q(created_article__range=(week_ago, today)))
        serializer_data = ArticleSerializer(articles, many=True)
        # print(serializer_data.data)
        self.assertEqual(response.data['results'], serializer_data.data)

    def test_auth_get_token(self):
        url = reverse('auth')
        response = self.client.post(url, {"username": self.user_2.email, "password": "131313!"})

        self.assertEqual(Token.objects.get(user=self.user_2).key, response.data['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_invalid(self):
        url = reverse('auth')
        response = self.client.post(url, {"username": self.user_2.email, "password": "blabla"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_auth_user(self):
        self.client.force_authenticate(user=self.user_2)
        response = self.client.post('/viewset/comment/',
                                    {'body': 'new idea', 'article': self.article_2.id, "author": self.user_2.id})
        self.assertGreater(self.article_2.comments_art.all().count(), 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_unauth_user(self):
        response = self.client.post('/viewset/comment/',
                                    {'body': 'new idea', 'article': self.article_2.id, "author": self.user_2.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_user_put_like(self):
        self.client.force_authenticate(user=self.user_2)
        url = f'/viewset/article/{self.article_1.id}/put_remove_like/'
        response = self.client.post(url)
        article = Article.objects.get(id=self.article_1.id)
        serializer_data = ArticleSerializer(article)
        self.assertGreater(self.article_1.likes.all().count(), 0)
        self.assertEqual(response.data, serializer_data.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauth_user_not_allowed_put_like(self):
        url = f'/viewset/article/{self.article_2.id}/put_remove_like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_isstaff_allow_create_article(self):
        self.client.force_authenticate(user=self.user_2)
        self.user_2.is_staff = True
        self.user_2.save()
        url = '/viewset/article/'
        response = self.client.post(url,
                                    {'title': 'test API title', 'body': "body text", 'categories': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auth_not_isstaff_deny_create_article(self):
        self.client.force_authenticate(user=self.user_2)

        url = '/viewset/article/'
        response = self.client.post(url,
                                    {'title': 'test API title', 'body': "body text", 'categories': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_auth_deny_create_article(self):
        url = '/viewset/article/'
        response = self.client.post(url,
                                    {'title': 'test API title', 'body': "body text", 'categories': self.category.id})
        self.assertEqual(response.status_code,  status.HTTP_401_UNAUTHORIZED)


    def test_auth_isstaff_allow_put_article(self):
        self.client.force_authenticate(user=self.user_1)
        self.user_1.is_staff = True
        self.user_1.save()
        url = f'/viewset/article/{self.article_1.id}/'
        response = self.client.put(url,
                                    {'title': 'Change', 'body': "Body has been changed", 'categories': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_not_isstaff_deny_put_article(self):
        self.client.force_authenticate(user=self.user_1)
        url = f'/viewset/article/{self.article_1.id}/'
        response = self.client.put(url,
                                   {'title': 'Change', 'body': "Body has been changed", 'categories': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_auth_deny_put_article(self):
        url = f'/viewset/article/{self.article_1.id}/'
        response = self.client.put(url,
                                   {'title': 'Change', 'body': "Body has been changed", 'categories': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_admin_deny_put_article_other_admin(self):
        self.client.force_authenticate(user=self.user_2)
        self.user_2.is_staff = True
        self.user_2.save()
        url = f'/viewset/article/{self.article_1.id}/'
        response = self.client.put(url,
                                   {'title': 'Change', 'body': "Body has been changed", 'categories': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_deny_delete_article_other_admin(self):
        self.client.force_authenticate(user=self.user_2)
        self.user_2.is_staff = True
        self.user_2.save()
        url = f'/viewset/article/{self.article_1.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_put(self):
        self.client.force_authenticate(user=self.user_2)
        url = f'/viewset/account/{self.user_2.id}/'
        response = self.client.put(url,{
            "email": "art@i.ua",
            "first_name": 'blabla',
            "last_name": "blablba"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_put_deny_another_admin(self):
        self.client.force_authenticate(user=self.user_2)
        url = f'/viewset/account/{self.user_1.id}/'
        response = self.client.put(url, {
            "email": "art@i.ua",
            "first_name": 'blabla',
            "last_name": "blablba"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_put_noauth_deny(self):
        url = f'/viewset/account/{self.user_2.id}/'
        response = self.client.put(url, {
            "email": "art@i.ua",
            "first_name": 'blabla',
            "last_name": "blablba"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_patch(self):
        self.client.force_authenticate(user=self.user_2)
        url = f'/viewset/account/{self.user_2.id}/'
        response = self.client.patch(url, {
            "first_name": 'lalalaal',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_patch_another_admin_deny(self):
        self.client.force_authenticate(user=self.user_2)
        url = f'/viewset/account/{self.user_1.id}/'
        response = self.client.patch(url, {
            "first_name": 'lalalaal',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_patch_noauth_deny(self):
        url = f'/viewset/account/{self.user_2.id}/'
        response = self.client.patch(url, {
            "first_name": 'lalalaal',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_subcriber_create_noauth(self):
        url = reverse("add-subscriber")
        response = self.client.post(url, {'email':'artem@i.ua'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subcriber_create_auth(self):
        self.client.force_authenticate(user=self.user_2)
        url = reverse("add-subscriber")
        response = self.client.post(url, {'email': self.user_2.email})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

