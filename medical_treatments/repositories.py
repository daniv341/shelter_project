from __future__ import annotations
from typing import Any
from medical_treatments.models import MedicalTreatment


class MedicalTreatmentRepository:
    def create(self, data: dict[str, Any]) -> MedicalTreatment:
        return MedicalTreatment.objects.create(**data)

    def update(self, medical_treatment: MedicalTreatment, data: dict[str, Any]) -> MedicalTreatment:
        for field, value in data.items():
            setattr(medical_treatment, field, value)
        medical_treatment.save()
        return medical_treatment

    def delete(self, medical_treatment: MedicalTreatment) -> None:
        medical_treatment.delete()
