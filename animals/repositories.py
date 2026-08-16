"""
repositories.py

Encapsula todas las operaciones de escritura sobre la base de datos
para el modelo Animal. No contiene lógica de negocio: solo persiste
lo que el servicio le indica.
"""
from __future__ import annotations

from typing import Any

from animals.models import Animal


class AnimalRepository:
    """Operaciones de escritura (create/update/delete) sobre Animal."""

    def create(self, data: dict[str, Any]) -> Animal:
        return Animal.objects.create(**data)

    def update(self, animal: Animal, data: dict[str, Any]) -> Animal:
        for field, value in data.items():
            setattr(animal, field, value)
        animal.save()
        return animal

    def delete(self, animal: Animal) -> None:
        animal.delete()
