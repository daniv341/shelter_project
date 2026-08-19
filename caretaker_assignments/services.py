from __future__ import annotations
from typing import Any
from caretaker_assignments.repositories import CaretakerAssignmentRepository
from caretaker_assignments.selectors import CaretakerAssignmentSelector


class CaretakerAssignmentService:
    def __init__(self, repository: CaretakerAssignmentRepository | None = None, selector: CaretakerAssignmentSelector | None = None) -> None:
        self.repository = repository or CaretakerAssignmentRepository()
        self.selector = selector or CaretakerAssignmentSelector()

    def list_caretaker_assignments(self):
        return self.selector.get_all()

    def get_caretaker_assignment(self, caretaker_assignment_id: str):
        return self.selector.get_by_id(caretaker_assignment_id)

    def create_caretaker_assignment(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_caretaker_assignment(self, caretaker_assignment_id: str, data: dict[str, Any]):
        caretaker_assignment = self.selector.get_by_id(caretaker_assignment_id)
        return self.repository.update(caretaker_assignment, data)

    def delete_caretaker_assignment(self, caretaker_assignment_id: str) -> None:
        caretaker_assignment = self.selector.get_by_id(caretaker_assignment_id)
        self.repository.delete(caretaker_assignment)
