"""
models.py

Únicamente entidades del ORM y validaciones propias del modelo.
No debe contener lógica de negocio (eso vive en services.py).
"""
from __future__ import annotations

from django.db import models
from django.utils import timezone
from ulid import ULID


def generate_ulid() -> str:
    """Genera un ULID como string, usado como PK del modelo Animal.

    Se eligió ULID (en vez de UUID o autoincremental) porque es
    ordenable lexicográficamente por tiempo de creación, lo cual es
    útil para paginar/ordenar sin depender de un campo adicional,
    y evita exponer IDs secuenciales predecibles.
    """
    return str(ULID())


class Animal(models.Model):
    class Sex(models.TextChoices):
        MALE = "male", "Macho"
        FEMALE = "female", "Hembra"
        UNKNOWN = "unknown", "Desconocido"

    class AdoptionStatus(models.TextChoices):
        AVAILABLE = "available", "Disponible"
        RESERVED = "reserved", "Reservado"
        ADOPTED = "adopted", "Adoptado"
        NOT_AVAILABLE = "not_available", "No disponible"

    class MedicalStatus(models.TextChoices):
        HEALTHY = "healthy", "Sano"
        IN_TREATMENT = "in_treatment", "En tratamiento"
        QUARANTINE = "quarantine", "Cuarentena"
        CRITICAL = "critical", "Crítico"

    id = models.CharField(
        primary_key=True,
        max_length=26,
        default=generate_ulid,
        editable=False,
    )
    name = models.CharField(max_length=150)
    species = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=Sex.choices)
    birth_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    admission_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    adoption_status = models.CharField(
        max_length=20,
        choices=AdoptionStatus.choices,
        default=AdoptionStatus.AVAILABLE,
    )
    medical_status = models.CharField(
        max_length=20,
        choices=MedicalStatus.choices,
        default=MedicalStatus.HEALTHY,
    )
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="animals/photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Animal"
        verbose_name_plural = "Animals"

    def __str__(self) -> str:
        return f"{self.name} ({self.species})"
