from __future__ import annotations
from typing import Any
from adoption_events.repositories import AdoptionEventRepository
from adoption_events.selectors import AdoptionEventSelector


class AdoptionEventService:
    def __init__(self, repository: AdoptionEventRepository | None = None, selector: AdoptionEventSelector | None = None) -> None:
        self.repository = repository or AdoptionEventRepository()
        self.selector = selector or AdoptionEventSelector()

    def list_adoption_events(self):
        return self.selector.get_all()

    def get_adoption_event(self, adoption_event_id: str):
        return self.selector.get_by_id(adoption_event_id)

    def create_adoption_event(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_adoption_event(self, adoption_event_id: str, data: dict[str, Any]):
        adoption_event = self.selector.get_by_id(adoption_event_id)
        return self.repository.update(adoption_event, data)

    def delete_adoption_event(self, adoption_event_id: str) -> None:
        adoption_event = self.selector.get_by_id(adoption_event_id)
        self.repository.delete(adoption_event)
