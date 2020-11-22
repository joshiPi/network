from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Follower, User, Post
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    """
    function returns index page and if request is post it creates the new post
    for current logged in user.

    """
    blogs = Post.objects.all()
    blogs = blogs[::-1]
    paginator = Paginator(blogs, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # return render(request, 'list.html', {'page_obj': page_obj})
    if request.method == "POST":
        content = request.POST["content"]

        if content:
            user = User.objects.get(id=request.user.id)
            a = Post(post_by=user, post_content=content)
            a.save()
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "network/index.html", {
                "message": "You can not create empty Post", "page_obj": page_obj
            })
    return render(request, "network/index.html", {
        "page_obj": page_obj, "message": ""
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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

# need to be changed not working as intended


@csrf_exempt
def edit_post(request, user, pk):
    """
    *returns JSON response so that javascript can detect whether to update the DOM or not

    allows user to edit post since the website is not reloaded 
    csrf exempt is used and value of edited post is saved in database
    but the actual value is not reflected until the page loads,
    using javascript value of that post is updated by manipulating DOM and when user reloads 
    the actual value is reflected.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")
        if content and content.strip():
            blog = Post.objects.filter(id=pk)
            blog.update(post_content=content)
            print(content)
            return JsonResponse({"message": "successfully updated"},
                                status=201)

        return JsonResponse({"message": "not_updated"},
                            status=201)

    if request.user.username == user:
        return JsonResponse({"message": "ok"}, status=201)
    return JsonResponse({"message": "not_ok"},
                        status=201)


def all_post(request):
    """
    Shows all post for all the users .
    """
    blogs = Post.objects.all()
    blogs = blogs[::-1]
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/all_post.html", {
        "page_obj": page_obj
    })


def all_following_post(request):
    """
    shows only those post which are written by the users 
    that the currently logged-in user follows.
    """
    name = request.user.username
    user = User.objects.get(username=name)
    follows = user.following.all()
    blogs = []
    for e in follows:
        f = e.following.created_by.all()
        for e in f:
            blogs.insert(0, e)
    if blogs != []:
        blogs = sorted(blogs, key=lambda post: post.created_at, reverse=True)
        paginator = Paginator(blogs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/all_post.html", {
            "page_obj": page_obj
        })
    return render(request, "network/all_post.html", {
        "message": "follow other users to get their post in your following feed"
    })


def like_unlike(request, pk):
    """
    *returns JSON response so that javascript can detect whether to update the DOM or not

    user can like and unlike post.

    """
    try:
        post = Post.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        post_liked_by = post.liked_by.all()
    except:
        return JsonResponse({"error": "not found."}, status=201)

    flag = 1
    for e in post_liked_by:
        if e.username == request.user.username:
            post.liked_by.remove(user)
            if post.post_likes >= 1:
                post.post_likes -= 1
                post.save()
                flag = 0
                return JsonResponse({"like_count": post.post_likes, "done": 'decrease'}, status=201)
    if flag:
        post.liked_by.add(user)
        post.post_likes += 1
        post.save()
        return JsonResponse({"like_count": post.post_likes, "done": 'increase'}, status=201)
    return JsonResponse({"error": "not found. wtf"}, status=404)


def user_profile(request, user):
    user = User.objects.get(username=user)
    blogs = user.created_by.all()
    blogs = blogs[::-1]
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/User.html", {
        "user": user, "page_obj": page_obj
    })


def follow_unfollow(request, query, user):
    """
    *returns JSON response so that javascript can detect whether to update the DOM or not

    let user folllow and unfollow any other user
    also checks that user cannot follow himself
    """
    user = User.objects.get(username=user)
    user_who_wants = User.objects.get(id=request.user.id)
    if request.user.username == user.username:
        return JsonResponse({"message": "you cannot follow or unfollow yourself"}, status=201)
    if query == "follow":
        followers = user.follower.all()
        for users in followers:
            if users.follower.username == request.user.username:
                return JsonResponse({"message": "you are already following this user"}, status=201)
        f = Follower(follower=request.user, following=user)
        f.save()
        return JsonResponse({"message": "you are now following this user"}, status=201)

    if query == "unfollow":
        followers = user.follower.all()
        for users in followers:
            if users.follower.username == request.user.username:
                f = Follower.objects.get(follower=request.user, following=user)
                f.delete()
                return JsonResponse({"message": "you unfollowed this user"}, status=201)
        return JsonResponse({"message": "you have to follow this user to unfollow"}, status=201)

    # return JsonResponse({"show": "working"}, status=201)
