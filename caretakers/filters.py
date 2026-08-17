import django_filters
from caretakers.models import Caretaker


class CaretakerFilter(django_filters.FilterSet):
    # filtrar por status
    class Meta:
        model = Caretaker
        fields = ["status"]