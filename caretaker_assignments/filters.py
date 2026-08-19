import django_filters
from caretaker_assignments.models import CaretakerAssignment


class CaretakerAssignmentFilter(django_filters.FilterSet):
    class Meta:
        model = CaretakerAssignment
        fields = ["animal", "caretaker", "status"]
