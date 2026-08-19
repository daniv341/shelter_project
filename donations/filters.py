import django_filters
from donations.models import Donation


class DonationFilter(django_filters.FilterSet):
    class Meta:
        model = Donation
        fields = ["adopter", "type_donation", "status"]
