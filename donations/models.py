from __future__ import annotations

from django.db import models
from ulid import ULID
from django.core.validators import MinValueValidator

from adopters.models import Adopter

def generate_ulid() -> str:
    return str(ULID())


class Donation(models.Model):
    # definir un enum para el estado de donation
    class Status(models.TextChoices):
        ACCEPT = "accept", "Aceptado"
        REJECTED = "rejected", "Rechazada"

    class Type_Donation(models.TextChoices):
        CASH = "cash", "Efectivo"
        TRANSFER = "transfer", "Transferencia"
        FOOD = "food", "Comida"
        OTHER = "other", "Otros"

    id = models.CharField(
            primary_key=True,
            max_length=26,
            default=generate_ulid,
            editable=False,
        )
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE, related_name="donations", db_index=True, blank=True, null=True)
    mount = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    type_donation = models.CharField(max_length=20, choices=Type_Donation.choices, default=Type_Donation.CASH)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACCEPT)
    donated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # definir el orden por defecto y los nombres en singular y plural
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

    # definir el metodo __str__
    def __str__(self) -> str:
        return f"{self.adopter} ({self.type_donation, self.mount})"
