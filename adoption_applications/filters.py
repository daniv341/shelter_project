import django_filters
from adoption_applications.models import AdoptionApplication


class AdoptionApplicationFilter(django_filters.FilterSet):
    class Meta:
        model = AdoptionApplication
        fields = ["animal", "adopter", "status"]
