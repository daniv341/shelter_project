from __future__ import annotations
#from django.utils import timezone esta libreria es necesaria tambien

from django.db import models
from ulid import ULID

from animals.models import Animal
from veterinarians.models import Veterinarian


def generate_ulid() -> str:
    return str(ULID())


class MedicalTreatment(models.Model):
    # definir un enum para el estado de medical_treatment
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        STARTED = "started", "Empezado"
        FINALIZED = "finalized", "Finalizado"

    id = models.CharField(
            primary_key=True,
            max_length=26,
            default=generate_ulid,
            editable=False,
        )
    diagnostic = models.CharField(max_length=100)
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, related_name="medical_treatments", db_index=True)
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.PROTECT, related_name="medical_treatments", db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    description = models.CharField(max_length=300, blank=True)
    #started_at = models.DateTimeField(default=timezone.now) asi se hace un atributo que tome la fecha actual de forma predeterminada
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # definir el orden por defecto y los nombres en singular y plural
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "MedicalTreatment"
        verbose_name_plural = "MedicalTreatments"

    # definir el metodo __str__
    def __str__(self) -> str:
        return f"{self.diagnostic} ({self.animal}, {self.veterinarian})"
