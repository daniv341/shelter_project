from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from veterinarians.models import Veterinarian


class VeterinarianSelector:
    def get_by_id(self, veterinarian_id: str) -> Veterinarian:
        return get_object_or_404(Veterinarian, pk=veterinarian_id)

    def get_all(self) -> QuerySet[Veterinarian]:
        return Veterinarian.objects.all()
