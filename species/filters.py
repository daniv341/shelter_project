import django_filters
from species.models import Species


class SpeciesFilter(django_filters.FilterSet):
    class Meta:
        model = Species
        fields = ["status"]
