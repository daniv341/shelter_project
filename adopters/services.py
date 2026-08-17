from __future__ import annotations
from typing import Any
from adopters.repositories import AdopterRepository
from adopters.selectors import AdopterSelector


class AdopterService:
    def __init__(self, repository: AdopterRepository | None = None, selector: AdopterSelector | None = None) -> None:
        self.repository = repository or AdopterRepository()
        self.selector = selector or AdopterSelector()

    def list_adopters(self):
        return self.selector.get_all()

    def get_adopter(self, adopter_id: str):
        return self.selector.get_by_id(adopter_id)

    def create_adopter(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_adopter(self, adopter_id: str, data: dict[str, Any]):
        adopter = self.selector.get_by_id(adopter_id)
        return self.repository.update(adopter, data)

    def delete_adopter(self, adopter_id: str) -> None:
        adopter = self.selector.get_by_id(adopter_id)
        self.repository.delete(adopter)
