from rest_framework import serializers
from newsapp.models import Article, Category, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class RetrieveSerialezer(serializers.ModelSerializer):
    article_likes = serializers.SerializerMethodField()
    article_comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title', 'annotation', 'body', 'image', 'comments', 'article_likes', 'article_comments']

    def get_article_likes(self, instance):
        return instance.likes.all().count()

    def get_article_comments(self, instance):
        return instance.comments.all().count()


class ArticleSerializer(serializers.ModelSerializer):
   # comments = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), write_only=True, many=True)
    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()


    class Meta:
        model = Article
        fields = ['title', 'body', 'created_article', 'author', 'categories', 'comments']

    def get_author(self, obj):
        return obj.author.email

    def get_categories(self, obj):
        return obj.categories.name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
   # article_id = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), write_only=True, many=True)
   tags_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), write_only=True, many=True)

   class Meta:
        model = Comment
        fields = ['id', 'body', 'article', 'tags_id']
        read_only_fields = ['id']

   def create(self, validated_data):
        article_id = validated_data.pop('article')
        #print(article_id.id)
        article = Article.objects.get(id=article_id.id)
        #article.comments.add(self.context['view'])
        print(self)
        return article
