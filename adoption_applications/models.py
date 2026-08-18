from __future__ import annotations

from django.db import models
from ulid import ULID

from adopters.models import Adopter
from animals.models import Animal


def generate_ulid() -> str:
    return str(ULID())


class AdoptionApplication(models.Model):
    # definir un enum para el estado de adoption_application
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Enviada"
        REVISION = "revision", "Revision"
        REJECTED = "rejected", "Rechazada"

    id = models.CharField(
            primary_key=True,
            max_length=26,
            default=generate_ulid,
            editable=False,
        )
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, related_name="adoption_applications", db_index=True)
    adopter = models.ForeignKey(Adopter, on_delete=models.PROTECT, related_name="adoption_applications", db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    submitted_at = models.DateTimeField(blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=350, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # definir el orden por defecto y los nombres en singular y plural
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "AdoptionApplication"
        verbose_name_plural = "AdoptionApplications"

    # definir el metodo __str__
    def __str__(self) -> str:
        return f"{self.status} ({self.animal}, {self.adopter})"
