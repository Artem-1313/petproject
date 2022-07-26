# Generated by Django 4.0.6 on 2022-07-26 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=300)),
                ('created_comment', models.DateField(auto_now_add=True)),
                ('update_comment', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('annotation', models.CharField(max_length=300)),
                ('body', models.TextField()),
                ('image', models.ImageField(default='images/default.jpg', upload_to='images')),
                ('created_article', models.DateField(auto_now_add=True)),
                ('update_article', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='article_categories', to='newsapp.category')),
                ('comments', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_comments', to='newsapp.comment')),
                ('likes', models.ManyToManyField(blank=True, default=None, related_name='article_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
