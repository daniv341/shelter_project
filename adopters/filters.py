import django_filters
from adopters.models import Adopter


class AdopterFilter(django_filters.FilterSet):
    class Meta:
        model = Adopter
        fields = ["status"]
