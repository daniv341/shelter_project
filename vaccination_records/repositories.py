from __future__ import annotations
from typing import Any
from vaccination_records.models import VaccinationRecord


class VaccinationRecordRepository:
    def create(self, data: dict[str, Any]) -> VaccinationRecord:
        return VaccinationRecord.objects.create(**data)

    def update(self, vaccination_record: VaccinationRecord, data: dict[str, Any]) -> VaccinationRecord:
        for field, value in data.items():
            setattr(vaccination_record, field, value)
        vaccination_record.save()
        return vaccination_record

    def delete(self, vaccination_record: VaccinationRecord) -> None:
        vaccination_record.delete()
