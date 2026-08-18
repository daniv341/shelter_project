from __future__ import annotations
from typing import Any
from adoption_applications.models import AdoptionApplication


class AdoptionApplicationRepository:
    def create(self, data: dict[str, Any]) -> AdoptionApplication:
        return AdoptionApplication.objects.create(**data)

    def update(self, adoption_application: AdoptionApplication, data: dict[str, Any]) -> AdoptionApplication:
        for field, value in data.items():
            setattr(adoption_application, field, value)
        adoption_application.save()
        return adoption_application

    def delete(self, adoption_application: AdoptionApplication) -> None:
        adoption_application.delete()
