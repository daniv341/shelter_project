from __future__ import annotations
from typing import Any
from veterinarians.models import Veterinarian


class VeterinarianRepository:
    def create(self, data: dict[str, Any]) -> Veterinarian:
        return Veterinarian.objects.create(**data)

    def update(self, veterinarian: Veterinarian, data: dict[str, Any]) -> Veterinarian:
        for field, value in data.items():
            setattr(veterinarian, field, value)
        veterinarian.save()
        return veterinarian

    def delete(self, veterinarian: Veterinarian) -> None:
        veterinarian.delete()
