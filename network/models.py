from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.username

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userposts")
    message = models.TextField(default="")
    date_post = models.DateTimeField(auto_now_add=False, default=datetime.now)
    likes = models.ManyToManyField(User, related_name='post_likes')
    status = models.BooleanField(default=False)

    def total_likes(self):
        return self.likes.count()

    def user_likes(self):
        return self.likes.all()

    def __str__(self):
        return f"{self.id} : {self.username} {self.message}"

class Follow(models.Model):
    f_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_following")
    follow = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.f_id} : {self.username} {self.follow} : {self.status}"
