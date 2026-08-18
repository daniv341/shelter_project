from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from adoption_applications.models import AdoptionApplication


class AdoptionApplicationSelector:
    def get_by_id(self, adoption_application_id: str) -> AdoptionApplication:
        return get_object_or_404(AdoptionApplication, pk=adoption_application_id)

    def get_all(self) -> QuerySet[AdoptionApplication]:
        return AdoptionApplication.objects.all()
