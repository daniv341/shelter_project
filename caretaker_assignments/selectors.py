from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from caretaker_assignments.models import CaretakerAssignment


class CaretakerAssignmentSelector:
    def get_by_id(self, caretaker_assignment_id: str) -> CaretakerAssignment:
        return get_object_or_404(CaretakerAssignment, pk=caretaker_assignment_id)

    def get_all(self) -> QuerySet[CaretakerAssignment]:
        return CaretakerAssignment.objects.all()
