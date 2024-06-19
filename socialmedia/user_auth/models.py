from django.db import models
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        primary_key=True,
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator, MinLengthValidator(4)],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    description = models.TextField(blank=True)
    status = models.CharField(max_length=511, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )

    friends = models.ManyToManyField("self", through='Friendship')

    REQUIRED_FIELDS = ["email", "first_name"]

    def is_subscribed_to(self, user):
        return Subscription.objects.filter(subscriber=self, subscribed_to=user).exists()

    def has_sent_friend_request(self, user):
        return FriendRequest.objects.filter(sender=self, receiver=user).exists()

    def has_received_friend_request(self, user):
        return user.has_sent_friend_request(self)

    def is_friends(self, user):
        return self.friends.filter(pk=user.pk).exists()

    def add_friend(self, user):
        if self == user:
            return
        friendship = Friendship.objects.get_or_create(user1=self, user2=user)
        return friendship

    # FUNCTIONAL

    def subscribe(self, user):
        subscription, created = Subscription.objects.get_or_create(subscriber=self, subscribed_to=user)
        return subscription

    def send_friend_request(self, user):
        if self.is_friends(user) or self.has_sent_friend_request(user):
            return
        if self.has_received_friend_request(user):
            user.unsend_friend_request(self)
            return self.add_friend(user)
        request = FriendRequest(sender=self, receiver=user)
        request.save()
        return request

    def unsend_friend_request(self, user):
        if not self.has_sent_friend_request(user):
            return
        request = FriendRequest.objects.get(sender=self, receiver=user)
        request.delete()


class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subscriptions", on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subscribers", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')


class Friendship(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friend1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friend2")
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_friend_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_friend_requests", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')
