from django.db import models
from django.conf import settings
from django.db.models import Count


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="post_like")
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="post_dislike")
    posted_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True, upload_to="post_images")

    class Meta:
        ordering = ["-posted_at"]

    def short_form(self):
        if len(self.content) <= 200:
            return str(self.content)
        return str(self.content)[:200] + '...'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="comment_like")
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="comment_dislike")
    posted_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["posted_at"]
