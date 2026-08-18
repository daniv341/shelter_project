from __future__ import annotations
from typing import Any
from adoption_applications.repositories import AdoptionApplicationRepository
from adoption_applications.selectors import AdoptionApplicationSelector


class AdoptionApplicationService:
    def __init__(self, repository: AdoptionApplicationRepository | None = None, selector: AdoptionApplicationSelector | None = None) -> None:
        self.repository = repository or AdoptionApplicationRepository()
        self.selector = selector or AdoptionApplicationSelector()

    def list_adoption_applications(self):
        return self.selector.get_all()

    def get_adoption_application(self, adoption_application_id: str):
        return self.selector.get_by_id(adoption_application_id)

    def create_adoption_application(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_adoption_application(self, adoption_application_id: str, data: dict[str, Any]):
        adoption_application = self.selector.get_by_id(adoption_application_id)
        return self.repository.update(adoption_application, data)

    def delete_adoption_application(self, adoption_application_id: str) -> None:
        adoption_application = self.selector.get_by_id(adoption_application_id)
        self.repository.delete(adoption_application)
