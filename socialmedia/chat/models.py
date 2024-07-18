from django.db import models
from django.conf import settings

class Conversation(models.Model):
    subject = models.CharField(max_length=255)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations")


class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
