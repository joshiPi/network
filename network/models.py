from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    post_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by")
    post_content = models.TextField()
    post_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        User, related_name="liked_by", blank=True)

    def __str__(self):
        return f"this post is created by {self.post_by} on {self.created_at}"


class Follower(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"
