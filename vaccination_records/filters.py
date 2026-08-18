import django_filters
from vaccination_records.models import VaccinationRecord


class VaccinationRecordFilter(django_filters.FilterSet):
    class Meta:
        model = VaccinationRecord
        fields = ["animal", "status"]
