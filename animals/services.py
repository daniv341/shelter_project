"""
services.py

Contiene toda la lógica de negocio del módulo animals. Las vistas
llaman únicamente a estos métodos; el servicio coordina el selector
(lecturas) y el repositorio (escrituras).
"""
from __future__ import annotations

from typing import Any

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from animals.models import Animal
from animals.repositories import AnimalRepository
from animals.selectors import AnimalSelector

from species.models import Species
from species.services import SpeciesService

class AnimalService:
    """Coordina la lógica de negocio relacionada con Animal."""

    def __init__(
        self,
        repository: AnimalRepository | None = None,
        selector: AnimalSelector | None = None,
    ) -> None:
        self.repository = repository or AnimalRepository()
        self.selector = selector or AnimalSelector()

    def list_animals(self) -> QuerySet[Animal]:
        return self.selector.get_all()

    def get_animal(self, animal_id: str) -> Animal:
        return self.selector.get_by_id(animal_id)

    def create_animal(self, data: dict[str, Any]) -> Animal:
        species = data.get("species")
        if species.status == Species.Status.BLOCKED:
            raise ValidationError("No se puede crear un Animal con una Species BLOCKED")
        return self.repository.create(data)

    def update_animal(self, animal_id: str, data: dict[str, Any]) -> Animal:
        animal = self.selector.get_by_id(animal_id) 
        new_adoption_status = data.get("adoption_status")
        adoption_status = animal.adoption_status
        medical_status = animal.medical_status

        if adoption_status == Animal.AdoptionStatus.ADOPTED:
            raise ValidationError("No se puede actualizar un Animal ADOPTED")
        if medical_status != Animal.MedicalStatus.HEALTHY and new_adoption_status == Animal.AdoptionStatus.ADOPTED:
            raise ValidationError("No se puede adoptar un Animal que no este HEALTHY")
        return self.repository.update(animal, data)

    def delete_animal(self, animal_id: str) -> None:
        animal = self.selector.get_by_id(animal_id)
        self.repository.delete(animal)
