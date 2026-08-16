from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from caretakers.models import Caretaker


class CaretakerSelector:
    def get_by_id(self, adopter_id: str) -> Caretaker:
        return get_object_or_404(Caretaker, pk=adopter_id)

    def get_all(self) -> QuerySet[Caretaker]:
        return Caretaker.objects.all()