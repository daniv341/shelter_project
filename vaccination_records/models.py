from __future__ import annotations

from django.db import models
from django.utils import timezone
from ulid import ULID

from animals.models import Animal

def generate_ulid() -> str:
    return str(ULID())


class VaccinationRecord(models.Model):
    # definir un enum para el estado de vaccination_record
    class Status(models.TextChoices):
        APPLIED = "applied", "Aplicado"
        PENDING = "pending", "Pendiente"
        CANCEL = "cancel", "Cancelado"

    id = models.CharField(
            primary_key=True,
            max_length=26,
            default=generate_ulid,
            editable=False,
        )
    name = models.CharField(max_length=200)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="vaccination_records", db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # definir el orden por defecto y los nombres en singular y plural
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "VaccinationRecord"
        verbose_name_plural = "VaccinationRecords"

    # definir el metodo __str__
    def __str__(self) -> str:
        return f"{self.name} ({self.animal})"
