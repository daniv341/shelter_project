from __future__ import annotations
from typing import Any
from veterinarians.repositories import VeterinatianRepository
from veterinarians.selectors import VeterinatianSelector


class VeterinatianService:
    def __init__(self, repository: VeterinatianRepository | None = None, selector: VeterinatianSelector | None = None) -> None:
        self.repository = repository or VeterinatianRepository()
        self.selector = selector or VeterinatianSelector()

    def list_veterinarians(self):
        return self.selector.get_all()

    def get_veterinatian(self, veterinatian_id: str):
        return self.selector.get_by_id(veterinatian_id)

    def create_veterinatian(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_veterinatian(self, veterinatian_id: str, data: dict[str, Any]):
        veterinatian = self.selector.get_by_id(veterinatian_id)
        return self.repository.update(veterinatian, data)

    def delete_veterinatian(self, veterinatian_id: str) -> None:
        veterinatian = self.selector.get_by_id(veterinatian_id)
        self.repository.delete(veterinatian)
