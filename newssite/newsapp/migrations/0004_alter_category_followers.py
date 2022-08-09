# Generated by Django 4.1 on 2022-08-09 20:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsapp', '0003_category_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='user_categories', to=settings.AUTH_USER_MODEL),
        ),
    ]
