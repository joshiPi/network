from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit/<str:user>/<int:pk>", views.edit_post, name="edit"),
    path("posts", views.all_post, name="posts"),
    path("like_unlike/<int:pk>", views.like_unlike, name="like_unlike"),
    path("following_post", views.all_following_post,
         name="following_post"),
    path("user_profile/<str:user>", views.user_profile, name="user_profile"),
    path("follow_unfollow/<str:query>/<str:user>",
         views.follow_unfollow, name="follow_unfollow")
]
