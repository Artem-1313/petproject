# Generated by Django 4.0.6 on 2022-08-01 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0003_remove_article_comments_comment_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='article',
        ),
        migrations.AddField(
            model_name='article',
            name='comments',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_comments', to='newsapp.comment'),
        ),
    ]
