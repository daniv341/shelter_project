from __future__ import annotations
from typing import Any
from adopters.models import Adopter


class AdopterRepository:
    def create(self, data: dict[str, Any]) -> Adopter:
        return Adopter.objects.create(**data)

    def update(self, adopter: Adopter, data: dict[str, Any]) -> Adopter:
        for field, value in data.items():
            setattr(adopter, field, value)
        adopter.save()
        return adopter

    def delete(self, adopter: Adopter) -> None:
        adopter.delete()
