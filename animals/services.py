"""
services.py

Contiene toda la lógica de negocio del módulo animals. Las vistas
llaman únicamente a estos métodos; el servicio coordina el selector
(lecturas) y el repositorio (escrituras).
"""
from __future__ import annotations

from typing import Any

from django.db.models import QuerySet

from animals.models import Animal
from animals.repositories import AnimalRepository
from animals.selectors import AnimalSelector


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
        # Punto de extensión: aquí irían reglas de negocio adicionales
        # (p.ej. validaciones cruzadas, notificaciones, auditoría) antes
        # de persistir el animal.
        return self.repository.create(data)

    def update_animal(self, animal_id: str, data: dict[str, Any]) -> Animal:
        animal = self.selector.get_by_id(animal_id)
        return self.repository.update(animal, data)

    def delete_animal(self, animal_id: str) -> None:
        animal = self.selector.get_by_id(animal_id)
        self.repository.delete(animal)
