from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from veterinarians.models import Veterinatian


class VeterinatianSelector:
    def get_by_id(self, veterinatian_id: str) -> Veterinatian:
        return get_object_or_404(Veterinatian, pk=veterinatian_id)

    def get_all(self) -> QuerySet[Veterinatian]:
        return Veterinatian.objects.all()
