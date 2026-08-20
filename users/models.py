from __future__ import annotations

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from ulid import ULID


def generate_ulid() -> str:
    return str(ULID())


class UserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None, **extra_fields):
        if not user_name:
            raise ValueError("El user_name es obligatorio")
        if not email:
            raise ValueError("El email es obligatorio")

        email = self.normalize_email(email)
        user = self.model(user_name=user_name, email=email, **extra_fields, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password=None, **extra_fields):
        extra_fields.setdefault("status", User.Status.ACTIVE)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(user_name=user_name, email=email, password=password, **extra_fields)


class User(AbstractBaseUser):
    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        BLOCKED = "blocked", "Bloqueado"

    id = models.CharField(
        primary_key=True,
        max_length=26,
        default=generate_ulid,
        editable=False,
    )
    user_name = models.CharField( max_length=200, unique=True)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    def __str__(self):
        return f"{self.user_name} ({self.status})"