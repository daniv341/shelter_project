from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from medical_treatments.models import MedicalTreatment


class MedicalTreatmentSelector:
    def get_by_id(self, medical_treatment_id: str) -> MedicalTreatment:
        return get_object_or_404(MedicalTreatment, pk=medical_treatment_id)

    def get_all(self) -> QuerySet[MedicalTreatment]:
        return MedicalTreatment.objects.all()
