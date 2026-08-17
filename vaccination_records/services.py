from __future__ import annotations
from typing import Any
from vaccination_records.repositories import VaccinationRecordRepository
from vaccination_records.selectors import VaccinationRecordSelector


class VaccinationRecordService:
    def __init__(self, repository: VaccinationRecordRepository | None = None, selector: VaccinationRecordSelector | None = None) -> None:
        self.repository = repository or VaccinationRecordRepository()
        self.selector = selector or VaccinationRecordSelector()

    def list_vaccination_records(self):
        return self.selector.get_all()

    def get_vaccination_record(self, vaccination_record_id: str):
        return self.selector.get_by_id(vaccination_record_id)

    def create_vaccination_record(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_vaccination_record(self, vaccination_record_id: str, data: dict[str, Any]):
        vaccination_record = self.selector.get_by_id(vaccination_record_id)
        return self.repository.update(vaccination_record, data)

    def delete_vaccination_record(self, vaccination_record_id: str) -> None:
        vaccination_record = self.selector.get_by_id(vaccination_record_id)
        self.repository.delete(vaccination_record)
