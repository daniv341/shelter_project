import django_filters
from caretakers.models import Caretaker


class CaretakerFilter(django_filters.FilterSet):

    class Meta:
        model = Caretaker
        fields = ["status"]