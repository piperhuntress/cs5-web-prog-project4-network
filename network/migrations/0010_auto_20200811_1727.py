# Generated by Django 3.0.8 on 2020-08-11 13:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
