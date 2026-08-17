from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from adopters.models import Adopter


class AdopterSelector:
    def get_by_id(self, adopter_id: str) -> Adopter:
        return get_object_or_404(Adopter, pk=adopter_id)

    def get_all(self) -> QuerySet[Adopter]:
        return Adopter.objects.all()
