from __future__ import annotations
from typing import Any
from rest_framework.exceptions import ValidationError

from adoption_events.repositories import AdoptionEventRepository
from adoption_events.selectors import AdoptionEventSelector

from adoption_events.models import AdoptionEvent
from adoption_applications.models import AdoptionApplication
from animals.models import Animal
from adopters.models import Adopter

class AdoptionEventService:
    def __init__(self, repository: AdoptionEventRepository | None = None, selector: AdoptionEventSelector | None = None) -> None:
        self.repository = repository or AdoptionEventRepository()
        self.selector = selector or AdoptionEventSelector()

    def list_adoption_events(self):
        return self.selector.get_all()

    def get_adoption_event(self, adoption_event_id: str):
        return self.selector.get_by_id(adoption_event_id)

    def create_adoption_event(self, data: dict[str, Any]):
        animal = data.get("animal")
        adopter = data.get("adopter")
        adoption_application = data.get("adoption_application")

        if animal.adoption_status == Animal.AdoptionStatus.ADOPTED:
            raise ValidationError("No se puede crear un Adoption Event con un Animal ADOPTED")
        if animal.medical_status != Animal.MedicalStatus.HEALTHY:
            raise ValidationError("No se puede crear un Adoption Event con un Animal que no este HEALTHY")
        if adopter.status == Adopter.Status.BLOCKED:
            raise ValidationError("No se puede crear un Adoption Event con un Adopter BLOCKED")
        if adoption_application.status != AdoptionApplication.Status.REVISION:
            raise ValidationError("No se puede crear un Adoption Event con una Adoption Application no en REVISION")
        return self.repository.create(data)

    def update_adoption_event(self, adoption_event_id: str, data: dict[str, Any]):
        adoption_event = self.selector.get_by_id(adoption_event_id)
        animal = adoption_event.animal
        adoption_application = adoption_event.adoption_application
        new_status = data.get("status")

        if adoption_event.status == AdoptionEvent.Status.CLOSED or adoption_event.status == AdoptionEvent.Status.REJECTED:
            raise ValidationError("No se puede actualizar un Adoption Event en el estado actual")
        
        if new_status == AdoptionEvent.Status.CLOSED:
            animal.adoption_status = Animal.AdoptionStatus.ADOPTED
            adoption_application.status = AdoptionApplication.Status.CLOSED
            animal.save(update_fields=["adoption_status"])
            adoption_application.save(update_fields=["status"])

        return self.repository.update(adoption_event, data)

    def delete_adoption_event(self, adoption_event_id: str) -> None:
        adoption_event = self.selector.get_by_id(adoption_event_id)
        self.repository.delete(adoption_event)
