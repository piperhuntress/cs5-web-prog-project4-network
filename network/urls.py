
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<str:u_name>", views.profile, name="profile"),
    path("like/<int:post_id>", views.like, name="like"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("follow/<str:profile_username>", views.follow, name="follow"),
    path("unfollow/<str:profile_username>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following")

]
