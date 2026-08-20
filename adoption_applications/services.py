from __future__ import annotations
from typing import Any
from rest_framework.exceptions import ValidationError

from adoption_applications.repositories import AdoptionApplicationRepository
from adoption_applications.selectors import AdoptionApplicationSelector

from adoption_applications.models import AdoptionApplication
from animals.models import Animal
from adopters.models import Adopter

class AdoptionApplicationService:
    def __init__(self, repository: AdoptionApplicationRepository | None = None, selector: AdoptionApplicationSelector | None = None) -> None:
        self.repository = repository or AdoptionApplicationRepository()
        self.selector = selector or AdoptionApplicationSelector()

    def list_adoption_applications(self):
        return self.selector.get_all()

    def get_adoption_application(self, adoption_application_id: str):
        return self.selector.get_by_id(adoption_application_id)

    def create_adoption_application(self, data: dict[str, Any]):
        animal = data.get("animal")
        adopter = data.get("adopter")

        if animal.adoption_status == Animal.AdoptionStatus.ADOPTED:
            raise ValidationError("No se puede crear un Adoption Applicationt con un Animal ADOPTED")
        if animal.medical_status != Animal.MedicalStatus.HEALTHY:
            raise ValidationError("No se puede crear un Adoption Applicationt con un Animal que no este HEALTHY")
        if adopter.status == Adopter.Status.BLOCKED:
            raise ValidationError("No se puede crear un Adoption Applicationt con un Adopter BLOCKED")
        
        return self.repository.create(data)

    def update_adoption_application(self, adoption_application_id: str, data: dict[str, Any]):
        adoption_application = self.selector.get_by_id(adoption_application_id)
        adoption_application_status = adoption_application.status

        if adoption_application_status == AdoptionApplication.Status.REJECTED or adoption_application_status == AdoptionApplication.Status.CLOSED:
            raise ValidationError("No se puede actualizar un Adoption Application en el estado actual")

        return self.repository.update(adoption_application, data)

    def delete_adoption_application(self, adoption_application_id: str) -> None:
        adoption_application = self.selector.get_by_id(adoption_application_id)
        self.repository.delete(adoption_application)
