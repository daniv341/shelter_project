from __future__ import annotations
from typing import Any
from rest_framework.exceptions import ValidationError
from species.repositories import SpeciesRepository
from species.selectors import SpeciesSelector

from species.models import Species
from animals.models import Animal

class SpeciesService:
    def __init__(self, repository: SpeciesRepository | None = None, selector: SpeciesSelector | None = None) -> None:
        self.repository = repository or SpeciesRepository()
        self.selector = selector or SpeciesSelector()

    def list_species(self):
        return self.selector.get_all()

    def get_species(self, species_id: str):
        return self.selector.get_by_id(species_id)

    def create_species(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_species(self, species_id: str, data: dict[str, Any]):
        species = self.selector.get_by_id(species_id)
        new_status = data.get("status")

        if new_status == Species.Status.BLOCKED and species.Status == Species.Status.ACTIVE:
            if Animal.objects.filter(species=species).exists():
                    raise ValidationError("No se puede eliminar una Species que todavia tenga Animals asociados")
        return self.repository.update(species, data)

    def delete_species(self, species_id: str) -> None:
        species = self.selector.get_by_id(species_id)
        self.repository.delete(species)
