import django_filters
from adoption_events.models import AdoptionEvent


class AdoptionEventFilter(django_filters.FilterSet):
    class Meta:
        model = AdoptionEvent
        fields = ["animal", "adopter", "adoption_application", "status"]
