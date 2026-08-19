from __future__ import annotations
from typing import Any
from caretaker_assignments.models import CaretakerAssignment


class CaretakerAssignmentRepository:
    def create(self, data: dict[str, Any]) -> CaretakerAssignment:
        return CaretakerAssignment.objects.create(**data)

    def update(self, caretaker_assignment: CaretakerAssignment, data: dict[str, Any]) -> CaretakerAssignment:
        for field, value in data.items():
            setattr(caretaker_assignment, field, value)
        caretaker_assignment.save()
        return caretaker_assignment

    def delete(self, caretaker_assignment: CaretakerAssignment) -> None:
        caretaker_assignment.delete()
