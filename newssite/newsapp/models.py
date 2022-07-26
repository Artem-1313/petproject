from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from newssite.celery import send_mail_category

User = get_user_model()
# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    annotation = models.CharField(max_length=300)
    body = models.TextField()
    image = models.ImageField(upload_to='images', default="images/default.jpg")
    top_news = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_article = models.DateField(auto_now_add=True)
    update_article = models.DateField(auto_now=True)
    categories = models.ForeignKey('Category', related_name='article_categories', on_delete=models.PROTECT)
   # comments = models.ManyToManyField('Comment', blank=True, related_name='article_comments', default=None )
    likes = models.ManyToManyField(User, related_name="article_likes", default=None, blank=True)

    def __str__(self):
        return f"{self.title}"

    @property
    def sum_of_likes(self):
        return self.likes.all().count()

    class Meta:
        verbose_name = "Новини"
        verbose_name_plural = "Новини"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    followers = models.ManyToManyField(User, related_name='user_categories', blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категорії"
        verbose_name_plural = "Категорії"




class Comment(models.Model):
    body = models.CharField(max_length=300)
    article = models.ForeignKey(Article, related_name="comments_art", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_comment = models.DateField(auto_now_add=True)
    update_comment = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.body[:20]}"

    class Meta:
        verbose_name = "Коментарі"
        verbose_name_plural = "Коментарі"


class Subscriber(models.Model):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Підписники"
        verbose_name_plural = "Підписники"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Article)
def create_article(sender, instance=None, created=False, **kwargs):
    if created:
        for follower in Category.objects.get(id=instance.categories.id).followers.all():
            send_mail_category.delay(instance.id, instance.categories.name, follower.email)









