import django_filters
from veterinarians.models import Veterinarian


class VeterinarianFilter(django_filters.FilterSet):
    class Meta:
        model = Veterinarian
        fields = ["status"]
