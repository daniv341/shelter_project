from __future__ import annotations

from django.db import models
from ulid import ULID


def generate_ulid() -> str:
    return str(ULID())


class Veterinatian(models.Model):
    # definir un enum para el estado de veterinatian
    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        BLOCKED = "blocked", "Bloqueado"

    id = models.CharField(
            primary_key=True,
            max_length=26,
            default=generate_ulid,
            editable=False,
        )
    full_name = models.CharField(max_length=200)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # definir el orden por defecto y los nombres en singular y plural
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Veterinatian"
        verbose_name_plural = "Veterinarians"

    # definir el metodo __str__
    def __str__(self) -> str:
        return f"{self.full_name} ({self.email})"
