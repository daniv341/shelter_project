from __future__ import annotations

from django.db import models
from ulid import ULID

from adopters.models import Adopter
from animals.models import Animal
from adoption_applications.models import AdoptionApplication

def generate_ulid() -> str:
    return str(ULID())


class AdoptionEvent(models.Model):
    # definir un enum para el estado de adoption_event
    class Status(models.TextChoices):
        ONGOING = "ongoing", "En Curso"
        REJECTED = "rejected", "Rechazada"
        CLOSED = "closed", "Cerrado"

    id = models.CharField(
            primary_key=True,
            max_length=26,
            default=generate_ulid,
            editable=False,
        )
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, related_name="adoption_event", db_index=True)
    adopter = models.ForeignKey(Adopter, on_delete=models.PROTECT, related_name="adoption_event", db_index=True)
    adoption_application = models.ForeignKey(AdoptionApplication, on_delete=models.PROTECT, related_name="adoption_event", db_index=True, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ONGOING)
    adopted_at = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=350, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # definir el orden por defecto y los nombres en singular y plural
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "AdoptionEvent"
        verbose_name_plural = "AdoptionEvents"

    # definir el metodo __str__
    def __str__(self) -> str:
        return f"{self.status} ({self.animal}, {self.adopter}, {self.adoption_application})"
