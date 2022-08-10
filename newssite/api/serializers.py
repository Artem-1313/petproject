from rest_framework import serializers
from newsapp.models import Article, Category, Comment, Subscriber
from django.contrib.auth import get_user_model

User = get_user_model()



class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email']

class ArticleAll(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'body', 'created_article']


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title', 'body', 'created_article', 'author', 'categories', 'likes']
        read_only_fields = ['likes']

    def get_author(self, obj):
        return obj.author.email

    def get_categories(self, obj):
        return obj.categories.name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'article', 'author']

class RetrieveSerialezer(serializers.ModelSerializer):

    article_likes = serializers.SerializerMethodField()
    article_comments = serializers.SerializerMethodField()
    comment = CommentSerializer(source="comments_art", many=True)

    class Meta:
        model = Article
        fields = ['title', 'annotation', 'body', 'image', 'article_likes', 'article_comments', 'comment']


    def get_article_likes(self, instance):
        return instance.likes.all().count()

    def get_article_comments(self, instance):
        return instance.comments_art.all().count()