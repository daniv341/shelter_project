from __future__ import annotations
from typing import Any
from rest_framework.exceptions import ValidationError

from donations.repositories import DonationRepository
from donations.selectors import DonationSelector

from adopters.models import Adopter

class DonationService:
    def __init__(self, repository: DonationRepository | None = None, selector: DonationSelector | None = None) -> None:
        self.repository = repository or DonationRepository()
        self.selector = selector or DonationSelector()

    def list_donations(self):
        return self.selector.get_all()

    def get_donation(self, donation_id: str):
        return self.selector.get_by_id(donation_id)

    def create_donation(self, data: dict[str, Any]):
        adopter = data.get("adopter")
        if adopter != None and adopter.status == Adopter.Status.BLOCKED:
            raise ValidationError("No se puede crear un Donation con una Adopter BLOCKED")
        return self.repository.create(data)

    def update_donation(self, donation_id: str, data: dict[str, Any]):
        donation = self.selector.get_by_id(donation_id)
        return self.repository.update(donation, data)

    def delete_donation(self, donation_id: str) -> None:
        donation = self.selector.get_by_id(donation_id)
        self.repository.delete(donation)
