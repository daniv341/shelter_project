from __future__ import annotations
from typing import Any
from donations.models import Donation


class DonationRepository:
    def create(self, data: dict[str, Any]) -> Donation:
        return Donation.objects.create(**data)

    def update(self, donation: Donation, data: dict[str, Any]) -> Donation:
        for field, value in data.items():
            setattr(donation, field, value)
        donation.save()
        return donation

    def delete(self, donation: Donation) -> None:
        donation.delete()
