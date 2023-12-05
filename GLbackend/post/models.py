import uuid

from django.conf import settings
from django.db import models
from django.forms import ValidationError  # profcheck
from django.utils.timesince import timesince
from django.utils import timezone


from .best_profanity import has_profanity  # models.py imports has_profanity from it
from django.apps import apps
from account.models import User
from django.contrib.auth import get_user_model
from django.db import models


class Like(models.Model):  # can reuse for liking pages or what (universal)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def created_at_formatted(self):
        return timesince(self.created_at)


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="post_attachments", blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name="post_attachments", on_delete=models.CASCADE
    )

    def get_image(self):
        if self.image:
            if self.image.url.startswith("http://") or self.image.url.startswith(
                "https://"
            ):
                return self.image.url
            return "http://127.0.0.1:8000" + self.image.url
        elif self.image_url:
            return self.image_url
        return ""  # Return a default image or an empty string if no image is set


class Category(models.Model):
    game_category = models.CharField(max_length=255)


class GameTitle(models.Model):
    title = models.CharField(max_length=255, unique=True)
    categories = models.ManyToManyField(Category)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    outside_id = models.CharField(max_length=100, unique=True, null=True)
    body = models.TextField(blank=True, null=True)
    game_title = models.ForeignKey(
        GameTitle, on_delete=models.PROTECT, blank=True, null=True
    )
    attachments = models.ManyToManyField(PostAttachment, blank=True)
    is_private = models.BooleanField(default=False)
    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)
    reported_by_users = models.ManyToManyField(User, blank=True)
    is_offensive = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE
    )  # all post will be deleted when this user is deleted

    post_url = models.TextField(blank=True, null=True)

    MENU_CHOICES = [
        ("discussions", "Discussions"),
        ("marketplace", "Marketplace"),
        ("connect", "Connect"),
        ("tournament", "Tournament"),
        ("beta", "Beta Testing"),
    ]

    menu = models.CharField(max_length=20, choices=MENU_CHOICES, default="Discussions")

    class Meta:
        ordering = ("-created_at",)  # order ng post sa feed

    def created_at_formatted(self):
        return timesince(self.created_at)

    # def clean(self):  # profcheck
    #     if has_profanity(self.body):
    #         self.save()  # profcheck
    #         raise ValidationError("Profanity detected")  # profcheck  # profcheck
    #         # has_profanity() is called in Post.clean() #profcheck
