from __future__ import annotations
from typing import Any
from species.models import Species


class SpeciesRepository:
    def create(self, data: dict[str, Any]) -> Species:
        return Species.objects.create(**data)

    def update(self, species: Species, data: dict[str, Any]) -> Species:
        for field, value in data.items():
            setattr(species, field, value)
        species.save()
        return species

    def delete(self, species: Species) -> None:
        species.delete()
