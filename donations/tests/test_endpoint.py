
from __future__ import annotations
import random
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from donations.models import Donation
from adopters.models import Adopter

pytestmark = pytest.mark.django_db

@pytest.fixture
def adopter(db):
    return Adopter.objects.create(full_name="rodrigo zurita", dni="12345678", status="active")

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def make_payload(adopter):
    def _make_payload(**overrides) -> dict:
        """Payload minimo valido para crear un donation (todos los campos requeridos)."""
        payload = {
                "adopter": adopter.id,
                "mount": random.randint(100, 10_000_000),
                "type_donation": Donation.Type_Donation.CASH,
                "status": Donation.Status.ACCEPT,
                "donated_at": "2026-08-17T19:16:27.889625",
        }
        payload.update(overrides)
        return payload

    return _make_payload

def make_optional_only_payload(**overrides) -> dict:
    """Payload solo con los campos requeridos, sin los opcionales."""
    payload = {
            "mount": random.randint(100, 10_000_000),
            "type_donation": Donation.Type_Donation.CASH,
            "status": Donation.Status.ACCEPT,
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def donation_payload(make_payload) -> dict:
    return make_payload()

@pytest.fixture
def donation_optional_payload() -> dict:
    return make_optional_only_payload()
    
@pytest.fixture
def created_donation(donation_payload, api_client) -> dict:
    response = api_client.post("/api/donations/", donation_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateDonation:
    def test_create_donation_success(self, donation_payload, api_client):
        response = api_client.post("/api/donations/", donation_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["adopter"]["id"] == donation_payload["adopter"]
        assert data["status"] == Donation.Status.ACCEPT
        assert "id" in data

    def test_create_donation_without_optional_fields(self, donation_optional_payload, api_client):
        response = api_client.post("/api/donations/", donation_optional_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["status"] == Donation.Status.ACCEPT
        assert data["mount"] == donation_optional_payload["mount"]

    def test_create_donation_missing_required_field(self, donation_payload, api_client):
        payload = donation_payload.copy()
        del payload["mount"]
        response = api_client.post("/api/donations/", payload, format="json")
        print(response.json)
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_donation_empty_required_field(self, donation_payload, api_client):
        payload = {**donation_payload, "mount": ""}
        response = api_client.post("/api/donations/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_donation_returns_timestamps(self, donation_optional_payload, api_client):
        response = api_client.post("/api/donations/", donation_optional_payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllDonations:
    def test_get_all_returns_paginated_list(self, api_client):
        response = api_client.get("/api/donations/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_donation(self, created_donation, api_client):
        response = api_client.get("/api/donations/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_donation["id"] in ids

    def test_get_all_donation_fields(self, created_donation, api_client):
        response = api_client.get("/api/donations/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_donation["id"]), None)
        assert item is not None
        for field in ("adopter", "type_donation", "status"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_donation, api_client):
        params = {"status": Donation.Status.ACCEPT}
        response = api_client.get("/api/donations/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == Donation.Status.ACCEPT


class TestGetDonationById:
    def test_get_donation_by_id_success(self, created_donation, api_client):
        donation_id = created_donation["id"]
        response = api_client.get(f"/api/donations/{donation_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == donation_id

    def test_get_donation_by_id_not_found(self, api_client):
        response = api_client.get("/api/donations/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_donation_by_id_returns_correct_data(self, created_donation, api_client):
        response = api_client.get(f"/api/donations/{created_donation['id']}/")
        data = response.data
        assert data["adopter"]["id"] == created_donation["adopter"]["id"]


class TestUpdateDonation:
    def test_update_donation_by_id_success(self, created_donation, api_client):
        donation_id = created_donation["id"]
        update_payload = {"status": Donation.Status.REJECTED}
        response = api_client.patch(f"/api/donations/{donation_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == Donation.Status.REJECTED

    def test_update_donation_by_id_not_found(self, api_client):
        response = api_client.patch(
            "/api/donations/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": Donation.Status.REJECTED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_donation_updates_updated_at(self, created_donation, api_client):
        donation_id = created_donation["id"]
        original_updated_at = created_donation["updated_at"]
        mount_updated = random.randint(100, 10_000_000)
        time.sleep(2)
        api_client.patch(f"/api/donations/{donation_id}/", {"mount": mount_updated}, format="json")
        response = api_client.get(f"/api/donations/{donation_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_donation_invalid_status(self, created_donation, api_client):
        response = api_client.patch(
            f"/api/donations/{created_donation['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteDonation:
    def test_delete_donation_by_id_success(self, donation_payload, api_client):
        create_resp = api_client.post("/api/donations/", donation_payload, format="json")
        donation_id = create_resp.data["id"]

        delete_resp = api_client.delete(f"/api/donations/{donation_id}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        get_resp = api_client.get(f"/api/donations/{donation_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_donation_by_id_not_found(self, api_client):
        response = api_client.delete("/api/donations/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_donation_by_id_idempotent(self, donation_payload, api_client):
        create_resp = api_client.post("/api/donations/", donation_payload, format="json")
        donation_id = create_resp.data["id"]
        api_client.delete(f"/api/donations/{donation_id}/")
        second_delete = api_client.delete(f"/api/donations/{donation_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND
