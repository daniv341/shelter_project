from __future__ import annotations
from typing import Any
from veterinarians.repositories import VeterinarianRepository
from veterinarians.selectors import VeterinarianSelector


class VeterinarianService:
    def __init__(self, repository: VeterinarianRepository | None = None, selector: VeterinarianSelector | None = None) -> None:
        self.repository = repository or VeterinarianRepository()
        self.selector = selector or VeterinarianSelector()

    def list_veterinarians(self):
        return self.selector.get_all()

    def get_veterinarian(self, veterinarian_id: str):
        return self.selector.get_by_id(veterinarian_id)

    def create_veterinarian(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_veterinarian(self, veterinarian_id: str, data: dict[str, Any]):
        veterinarian = self.selector.get_by_id(veterinarian_id)
        return self.repository.update(veterinarian, data)

    def delete_veterinarian(self, veterinarian_id: str) -> None:
        veterinarian = self.selector.get_by_id(veterinarian_id)
        self.repository.delete(veterinarian)
