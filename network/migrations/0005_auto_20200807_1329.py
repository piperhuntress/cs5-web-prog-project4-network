# Generated by Django 3.0.8 on 2020-08-07 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_post_likes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Follower',
            new_name='Follow',
        ),
    ]
