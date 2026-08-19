from __future__ import annotations

from django.db import models
from ulid import ULID

from animals.models import Animal
from caretakers.models import Caretaker

def generate_ulid() -> str:
    return str(ULID())

#esta es una relacion N:N, la otra parte de la relacion esta en animals model, solo es necesario de un lado, no hace falta en caretakers

class CaretakerAssignment(models.Model):
    # definir un enum para el estado de caretaker_assignment
    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        FINISHED = "finished", "Terminado"

    id = models.CharField(
            primary_key=True,
            max_length=26,
            default=generate_ulid,
            editable=False,
        )
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="caretaker_assignments", db_index=True)
    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE, related_name="caretaker_assignments", db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    assignment_at = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=350, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # definir el orden por defecto y los nombres en singular y plural
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "CaretakerAssignment"
        verbose_name_plural = "CaretakerAssignments"

    # definir el metodo __str__
    def __str__(self) -> str:
        return f"{self.status} ({self.animal}, {self.caretaker})"
