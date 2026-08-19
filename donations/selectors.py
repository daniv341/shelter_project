from __future__ import annotations
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from donations.models import Donation


class DonationSelector:
    def get_by_id(self, donation_id: str) -> Donation:
        return get_object_or_404(Donation, pk=donation_id)

    def get_all(self) -> QuerySet[Donation]:
        return Donation.objects.all()
