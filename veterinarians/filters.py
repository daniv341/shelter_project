import django_filters
from veterinarians.models import Veterinatian


class VeterinatianFilter(django_filters.FilterSet):
    class Meta:
        model = Veterinatian
        fields = ["status"]
