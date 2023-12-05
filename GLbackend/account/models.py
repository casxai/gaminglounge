from typing import Any
import uuid  # unique identification for the users

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils.timesince import timesince
from django.utils import timezone
from django.contrib.auth import get_user_model


class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("you have not provided a valid email address :<")

        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        name = input("Enter the name for the superuser: ")
        return self._create_user(name, email, password, **extra_fields)


class User(
    AbstractBaseUser, PermissionsMixin
):  # user model for creating users from models
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # uses the uuid from the top
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, default="")
    friends = models.ManyToManyField("self")
    friends_count = models.IntegerField(default=0)
    pref_game_category = models.TextField(blank=True, null=True)
    pref_game_titles = models.TextField(blank=True, null=True)

    people_you_may_know = models.ManyToManyField("self")

    posts_count = models.IntegerField(default=0)

    is_active = models.BooleanField(
        default=True
    )  # checking if the user is active, soon set to false for verification
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    charisma_score = models.IntegerField(default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def is_close_to_ban(self):
        ban_threshold = -5
        close_threshold = -3

        if self.charisma_score <= close_threshold and self.charisma_score > ban_threshold:
            return True
        return False

    def ban_user(self):
            if self.charisma_score <= -5:
                self.is_active = False
            else:
                self.is_active = True
            self.save(update_fields=["is_active"])

    def calculate_charisma_score(self):
        # Calculate charisma based on the number of likes on the user's posts
        total_likes_received = sum(post.likes_count for post in self.posts.all())

        # Calculate charisma based on the number of comments received by other users
        total_comments_received = sum(post.comments_count for post in self.posts.all())

        # Calculate charisma based on the number of friends
        total_friends = self.friends_count

        total_posts = self.posts.count()

        offensive_posts_count = self.posts.filter(is_offensive=True).count()
            
        # Calculate the charisma score
        charisma_score = (
            (total_likes_received * 5)
            + (total_comments_received * 3)
            + (total_friends * 2)
            # + (total_posts * 1)
            - (offensive_posts_count * 1)
        )

        self.charisma_score = charisma_score
        self.save(update_fields=["charisma_score"])

        return charisma_score

    def get_avatar(self):
        if self.avatar:
            return settings.WEBSITE_URL + self.avatar.url
        else:
            default_avatar_path = "/media/avatars/default.jpg"
        return settings.WEBSITE_URL + default_avatar_path


class FriendshipRequest(models.Model):
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

    STATUS_CHOICES = (
        (SENT, "sent"),
        (ACCEPTED, "accepted"),
        (REJECTED, "rejected"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_for = models.ForeignKey(
        User, related_name="received_friendshiprequests", on_delete=models.CASCADE
    )  # friend request sent to
    created_by = models.ForeignKey(
        User, related_name="created_friendshiprequests", on_delete=models.CASCADE
    )  # who made the friend request
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)


class UserVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visited_page = models.CharField(max_length=255)
    visit_datetime = models.DateTimeField(auto_now_add=True)
