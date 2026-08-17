from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from vaccination_records.models import VaccinationRecord


class VaccinationRecordSelector:
    def get_by_id(self, vaccination_record_id: str) -> VaccinationRecord:
        return get_object_or_404(VaccinationRecord, pk=vaccination_record_id)

    def get_all(self) -> QuerySet[VaccinationRecord]:
        return VaccinationRecord.objects.select_related("animal")
