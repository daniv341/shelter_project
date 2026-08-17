from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from species.models import Species


class SpeciesSelector:
    def get_by_id(self, species_id: str) -> Species:
        return get_object_or_404(Species, pk=species_id)

    def get_all(self) -> QuerySet[Species]:
        return Species.objects.all()
