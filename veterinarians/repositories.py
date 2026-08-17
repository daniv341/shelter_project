from __future__ import annotations
from typing import Any
from veterinarians.models import Veterinatian


class VeterinatianRepository:
    def create(self, data: dict[str, Any]) -> Veterinatian:
        return Veterinatian.objects.create(**data)

    def update(self, veterinatian: Veterinatian, data: dict[str, Any]) -> Veterinatian:
        for field, value in data.items():
            setattr(veterinatian, field, value)
        veterinatian.save()
        return veterinatian

    def delete(self, veterinatian: Veterinatian) -> None:
        veterinatian.delete()
