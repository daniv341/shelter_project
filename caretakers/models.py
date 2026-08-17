from __future__ import annotations

from django.db import models
from ulid import ULID

def generate_ulid() -> str:
    return str(ULID())

class Caretaker(models.Model):
    # definir un enum para el estado del caretaker
    class Status(models.TextChoices):
        # el valor active se guardará en la base de datos, mientras que el valor "Activo" se mostrará en el admin
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
        verbose_name = "Caretaker"
        verbose_name_plural = "Caretakers"

    # definir el método __str__ para mostrar el nombre completo y el email del caretaker
    def __str__(self) -> str:
        return f"{self.full_name} ({self.email})"