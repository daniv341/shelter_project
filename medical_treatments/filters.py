import django_filters
from medical_treatments.models import MedicalTreatment


class MedicalTreatmentFilter(django_filters.FilterSet):
    class Meta:
        model = MedicalTreatment
        fields = ["animal", "veterinarian", "status"]
