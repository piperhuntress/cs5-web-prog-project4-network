from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .models import User, Post, Follow

num_posts = 10

@login_required(login_url='/login')
def index(request):
    posts_list = Post.objects.all().order_by('-date_post')
    paginator = Paginator(posts_list, num_posts) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = User.objects.get(username=request.user)
    followers_list = Follow.objects.filter(follow=user, status=True)

    return render(request, 'network/index.html', {
        'page_obj': page_obj,
        'total_post': posts_list.count(),
        'followers_list': followers_list,
        'followed_user':user

    })

def liked(user_id, post_id):
    post = Post.objects.get(pk=int(post_id))
    if post.likes.filter(id=user_id).exists():
        liked = False
    else:
        liked = True
    return liked

@ensure_csrf_cookie
@login_required(login_url='/login')
def like(request, post_id):
    print(post_id)
    post = Post.objects.get(pk=int(post_id))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        post.status = False;
        post.save()
        return JsonResponse({
            "liked": "False",
            "total_likes": post.total_likes(),
        })
    else:
        post.likes.add(request.user)
        post.status = True;
        post.save()
        return JsonResponse({
            "liked": "True",
            "total_likes": post.total_likes(),
        })

@login_required(login_url='/login')
def edit(request, post_id):
    user = User.objects.get(username=request.user)
    followers_list = Follow.objects.filter(follow=user, status=True)

    if request.method == "POST":
        post = Post.objects.get(pk=int(post_id))
        data = json.loads(request.body)
        print(data)
        post.message = data.get('post_message');
        post.save()
        return JsonResponse({
            "status": "Post Edited.",
            "message": post.message
            })
    elif request.method == "GET":
        print('test')
        try:
            post = Post.objects.get(pk=int(post_id))
        except Post.DoesNotExist:
            return render(request, "network/error.html", {
                "message": "Error: Post does not exist.",
                "followers_list": followers_list,
                'followed_user':user
            })

        if(post.username != request.user.username):
            return render(request, "network/error.html", {
                "message": "Error: Not allowed to edit.",
                "followers_list": followers_list,
                'followed_user':user
            })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='/login')
def newpost(request):
    if request.method == "POST":
        p_message = request.POST["message"]
        user = request.user
        post = Post(message=p_message,username=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
def profile(request, u_name):
    try:
        user_profile = User.objects.get(username = u_name)
        posts_list = Post.objects.filter(username=user_profile.id).order_by('-date_post')
        follow =Follow.objects.filter(username=request.user, follow=user_profile) # get the follow object of this user and the user to be followed
        following = Follow.objects.filter(username=user_profile, status=True).count()
        followers = Follow.objects.filter(follow=user_profile, status=True).count()
        paginator = Paginator(posts_list, num_posts)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        user = User.objects.get(username=u_name)
        followers_list = Follow.objects.filter(follow=user, status=True) #get the names of the followers

    except Post.DoesNotExist:
        raise Http404("User not found.")
    return render(request, "network/profile.html",{
        'page_obj': page_obj,
        "profile" : user_profile,
        "follows": follow,
        "following" : following,
        "followers" : followers,
        'followers_list': followers_list,
        "followed_user": user

    })

@login_required(login_url='/login')
def follow(request, profile_username):
    if request.method == "POST":
        user_profile = User.objects.get(username = profile_username)
        follow_profile = Follow.objects.filter(username=request.user, follow=user_profile)
        if(not follow_profile):
            follow_profile = Follow(username=request.user, follow=user_profile, status=True)
            follow_profile.save()
        else:
            f_profile = Follow.objects.get(f_id=follow_profile[0].f_id)
            f_profile.status=True
            f_profile.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'u_name':profile_username}))

@login_required(login_url='/login')
def unfollow(request, profile_username):
    if request.method == "POST":
        user_profile = User.objects.get(username = profile_username)
        follow_profile = Follow.objects.filter(username=request.user, follow=user_profile)
        f_profile = Follow.objects.get(f_id=follow_profile[0].f_id)
        f_profile.status=False
        print(follow_profile[0].f_id)
        f_profile.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'u_name':profile_username}))

@login_required(login_url='/login')
def following(request):
        user = User.objects.get(username=request.user)
        follow = Follow.objects.filter(username=user, status=True)
        user_ids = []
        posts = []
        for user_follow in follow:
            user_followed_id = User.objects.get(username=user_follow.follow).pk
            user_ids.append(user_followed_id)
        posts_list = Post.objects.filter(username__in=user_ids).order_by('-date_post')
        paginator = Paginator(posts_list, num_posts)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        user = User.objects.get(username=user)
        followers_list = Follow.objects.filter(follow=user, status=True) #get the names of the followers


        return render(request, 'network/index.html', {
            'page_obj': page_obj,
            'followers_list': followers_list,
            "followed_user": user
        })
