from __future__ import annotations

from django.db import models
from ulid import ULID
from django.core.validators import MaxValueValidator, MinValueValidator

def generate_ulid() -> str:
    return str(ULID())


class Veterinarian(models.Model):
    # definir un enum para el estado de veterinarian
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
    dni = models.PositiveBigIntegerField(unique=True, validators=[MinValueValidator(1_000_000), MaxValueValidator(99_999_999)])
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.PositiveBigIntegerField(unique=True, validators=[MinValueValidator(100_000)], blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # definir el orden por defecto y los nombres en singular y plural
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Veterinarian"
        verbose_name_plural = "Veterinarians"

    # definir el metodo __str__
    def __str__(self) -> str:
        return f"{self.full_name} ({self.email})"
