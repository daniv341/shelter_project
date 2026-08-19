from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from adoption_events.models import AdoptionEvent


class AdoptionEventSelector:
    def get_by_id(self, adoption_event_id: str) -> AdoptionEvent:
        return get_object_or_404(AdoptionEvent, pk=adoption_event_id)

    def get_all(self) -> QuerySet[AdoptionEvent]:
        return AdoptionEvent.objects.all()
