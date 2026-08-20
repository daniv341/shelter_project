
from __future__ import annotations
import time
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def make_payload(**overrides) -> dict:
    """Payload minimo valido para crear un user (todos los campos requeridos)."""
    payload = {
        "user_name": f"test_{uuid.uuid4().hex[:5]}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "password": "orion el gatito mas bonito"
    }
    payload.update(overrides)
    return payload

@pytest.fixture
def user_payload() -> dict:
    return make_payload()
    
@pytest.fixture
def created_user(user_payload, api_client) -> dict:
    response = api_client.post("/api/users/", user_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Setup fallo: {response.data}"
    return response.data


class TestCreateUser:
    def test_create_user_success(self, user_payload, api_client):
        response = api_client.post("/api/users/", user_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert data["user_name"] == user_payload["user_name"]
        assert data["status"] == User.Status.ACTIVE
        assert "id" in data

    def test_create_user_missing_required_field(self, user_payload, api_client):
        payload = user_payload.copy()
        del payload["user_name"]
        response = api_client.post("/api/users/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_empty_required_field(self, user_payload, api_client):
        payload = {**user_payload, "user_name": ""}
        response = api_client.post("/api/users/", payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_returns_timestamps(self, user_payload, api_client):
        response = api_client.post("/api/users/", user_payload, format="json")
        data = response.data
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllUsers:
    def test_get_all_returns_paginated_list(self, authenticated_client):
        response = authenticated_client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_get_all_contains_created_user(self, created_user, authenticated_client):
        response = authenticated_client.get("/api/users/")
        results = response.data["results"]
        ids = [item["id"] for item in results]
        assert created_user["id"] in ids

    def test_get_all_user_fields(self, created_user, authenticated_client):
        response = authenticated_client.get("/api/users/")
        results = response.data["results"]
        item = next((p for p in results if p["id"] == created_user["id"]), None)
        assert item is not None
        for field in ("user_name", "email"):
            assert field in item

    def test_get_all_filtering_by_status(self, created_user, authenticated_client):
        params = {"status": User.Status.ACTIVE}
        response = authenticated_client.get("/api/users/", params)
        results = response.data["results"]
        assert len(results) > 0
        for item in results:
            assert item["status"] == User.Status.ACTIVE

    def test_get_all_requires_authentication(self, api_client):
        response = api_client.get("/api/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetUserById:
    def test_get_user_by_id_success(self, created_user, authenticated_client):
        user_id = created_user["id"]
        response = authenticated_client.get(f"/api/users/{user_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == user_id

    def test_get_user_by_id_not_found(self, authenticated_client):
        response = authenticated_client.get("/api/users/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_user_by_id_returns_correct_data(self, created_user, authenticated_client):
        response = authenticated_client.get(f"/api/users/{created_user['id']}/")
        data = response.data
        assert data["user_name"] == created_user["user_name"]


class TestUpdateUser:
    def test_update_user_by_id_success(self, created_user, staff_client):
        user_id = created_user["id"]
        update_payload = {"status": User.Status.BLOCKED}
        response = staff_client.patch(f"/api/users/{user_id}/", update_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["status"] == User.Status.BLOCKED

    def test_update_user_by_id_not_found(self, staff_client):
        response = staff_client.patch(
            "/api/users/01ARZ3NDEKTSV4RRFFQ69G5FAV/",
            {"status": User.Status.BLOCKED},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_updates_updated_at(self, created_user, staff_client):
        user_id = created_user["id"]
        original_updated_at = created_user["updated_at"]
        time.sleep(2)
        staff_client.patch(f"/api/users/{user_id}/", {"user_name": "Valor actualizado"}, format="json")
        response = staff_client.get(f"/api/users/{user_id}/")
        new_updated_at = response.data["updated_at"]
        assert new_updated_at > original_updated_at

    def test_update_user_invalid_status(self, created_user, staff_client):
        response = staff_client.patch(
            f"/api/users/{created_user['id']}/", {"status": "INVALID"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_user_requires_staff(self, created_user, authenticated_client):
        response = authenticated_client.patch(f"/api/users/{created_user['id']}/", {"status": User.Status.BLOCKED}, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestDeleteUser:
    def test_delete_user_by_id_success(self, user_payload, staff_client):
        response = staff_client.post("/api/users/", user_payload, format="json")
        user_id = response.data["id"]
        delete_resp = staff_client.delete(f"/api/users/{user_id}/")
        print(response.data)
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT
        get_resp = staff_client.get(f"/api/users/{user_id}/")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_by_id_not_found(self, staff_client):
        response = staff_client.delete("/api/users/01ARZ3NDEKTSV4RRFFQ69G5FAV/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_by_id_idempotent(self, user_payload, staff_client):
        response = staff_client.post("/api/users/", user_payload, format="json")
        user_id = response.data["id"]
        staff_client.delete(f"/api/users/{user_id}/")
        second_delete = staff_client.delete(f"/api/users/{user_id}/")
        assert second_delete.status_code == status.HTTP_404_NOT_FOUND
