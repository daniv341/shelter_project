from __future__ import annotations
from typing import Any
from medical_treatments.repositories import MedicalTreatmentRepository
from medical_treatments.selectors import MedicalTreatmentSelector


class MedicalTreatmentService:
    def __init__(self, repository: MedicalTreatmentRepository | None = None, selector: MedicalTreatmentSelector | None = None) -> None:
        self.repository = repository or MedicalTreatmentRepository()
        self.selector = selector or MedicalTreatmentSelector()

    def list_medical_treatments(self):
        return self.selector.get_all()

    def get_medical_treatment(self, medical_treatment_id: str):
        return self.selector.get_by_id(medical_treatment_id)

    def create_medical_treatment(self, data: dict[str, Any]):
        return self.repository.create(data)

    def update_medical_treatment(self, medical_treatment_id: str, data: dict[str, Any]):
        medical_treatment = self.selector.get_by_id(medical_treatment_id)
        return self.repository.update(medical_treatment, data)

    def delete_medical_treatment(self, medical_treatment_id: str) -> None:
        medical_treatment = self.selector.get_by_id(medical_treatment_id)
        self.repository.delete(medical_treatment)
