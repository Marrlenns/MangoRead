from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from manga.models import Book


class CustomUserManager(BaseUserManager):
    """Custom User Manager for creating users and superusers."""
    def create_user(self, username, password, **extra_fields):
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_stuff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(username=username, password=password, **extra_fields)


class User(AbstractUser):
    """Custom User Model with additional fields"""
    image = models.ImageField(null=True, blank=True, upload_to="avatarki")
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50)

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["image", "nickname"]

    def __str__(self):
        return self.username


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comment")
    text = models.TextField()

    def __str__(self):
        return f"{self.author} - {self.book.title}"