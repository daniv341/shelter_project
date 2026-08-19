from __future__ import annotations
from typing import Any
from adoption_events.models import AdoptionEvent


class AdoptionEventRepository:
    def create(self, data: dict[str, Any]) -> AdoptionEvent:
        return AdoptionEvent.objects.create(**data)

    def update(self, adoption_event: AdoptionEvent, data: dict[str, Any]) -> AdoptionEvent:
        for field, value in data.items():
            setattr(adoption_event, field, value)
        adoption_event.save()
        return adoption_event

    def delete(self, adoption_event: AdoptionEvent) -> None:
        adoption_event.delete()
