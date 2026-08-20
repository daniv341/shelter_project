from __future__ import annotations
from typing import Any
from rest_framework.exceptions import ValidationError

from caretaker_assignments.repositories import CaretakerAssignmentRepository
from caretaker_assignments.selectors import CaretakerAssignmentSelector

from caretaker_assignments.models import CaretakerAssignment
from animals.models import Animal
from caretakers.models import Caretaker

class CaretakerAssignmentService:
    def __init__(self, repository: CaretakerAssignmentRepository | None = None, selector: CaretakerAssignmentSelector | None = None) -> None:
        self.repository = repository or CaretakerAssignmentRepository()
        self.selector = selector or CaretakerAssignmentSelector()

    def list_caretaker_assignments(self):
        return self.selector.get_all()

    def get_caretaker_assignment(self, caretaker_assignment_id: str):
        return self.selector.get_by_id(caretaker_assignment_id)

    def create_caretaker_assignment(self, data: dict[str, Any]):
        animal = data.get("animal")
        caretaker = data.get("caretaker")

        if CaretakerAssignment.objects.filter(animal=animal, caretaker=caretaker, status=CaretakerAssignment.Status.ACTIVE).exists():
            raise ValidationError("El Animal ya esta asignado a este Caretaker")

        if animal.adoption_status != Animal.AdoptionStatus.RESERVED:
            raise ValidationError("No se puede crear un Assignment Caretaker con un Animal no RESERVED")
        if caretaker.status == Caretaker.Status.BLOCKED:
            raise ValidationError("No se puede crear un Assignment Caretaker con un Caretaker BLOCKED")

        animal.adoption_status = Animal.AdoptionStatus.NOT_AVAILABLE
        animal.save(update_fields=["adoption_status"])

        return self.repository.create(data)

    def update_caretaker_assignment(self, caretaker_assignment_id: str, data: dict[str, Any]):
        caretaker_assignment = self.selector.get_by_id(caretaker_assignment_id)
        animal = caretaker_assignment.animal
        new_status = data.get("status")
        if new_status == CaretakerAssignment.Status.FINISHED:
            animal.adoption_status = Animal.AdoptionStatus.RESERVED
            animal.save(update_fields=["adoption_status"])
        return self.repository.update(caretaker_assignment, data)

    def delete_caretaker_assignment(self, caretaker_assignment_id: str) -> None:
        caretaker_assignment = self.selector.get_by_id(caretaker_assignment_id)
        self.repository.delete(caretaker_assignment)
