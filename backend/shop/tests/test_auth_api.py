import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_jwt_obtain_and_refresh():
    User.objects.create_user(username="demo", password="pass12345")
    client = APIClient()

    resp = client.post("/api/auth/jwt/create/", {"username": "demo", "password": "pass12345"}, format="json")
    assert resp.status_code == 200
    tokens = resp.json()
    assert "access" in tokens and "refresh" in tokens

    resp = client.post("/api/auth/jwt/refresh/", {"refresh": tokens["refresh"]}, format="json")
    assert resp.status_code == 200
    assert "access" in resp.json()


@pytest.mark.django_db
def test_protected_endpoint_requires_auth():
    client = APIClient()
    resp = client.post("/api/products/", {}, format="json")
    assert resp.status_code in (401, 403)


