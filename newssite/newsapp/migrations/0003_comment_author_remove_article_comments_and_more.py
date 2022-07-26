# Generated by Django 4.0.6 on 2022-07-26 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsapp', '0002_alter_article_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='article',
            name='comments',
        ),
        migrations.AddField(
            model_name='article',
            name='comments',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='article_comments', to='newsapp.comment'),
        ),
    ]
