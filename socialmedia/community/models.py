from django.db import models
from django.conf import settings


class Community(models.Model):
    administrator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="communities")
    moderator = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="moderated_communities")
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followed_communities")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to="community_images")
    only_staff_post = models.BooleanField(default=True)
