# Generated by Django 3.2.14 on 2022-08-03 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0002_remove_comment_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='comments',
        ),
    ]
