import pytest
from rest_framework.test import APIClient
from shop.models import Category


@pytest.mark.django_db
def test_list_categories():
    Category.objects.create(name="Books", slug="books")
    Category.objects.create(name="Clothing", slug="clothing")

    client = APIClient()
    response = client.get("/api/categories/")

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2
    assert data["results"][0]["name"] in ["Books", "Clothing"]


@pytest.mark.django_db
def test_create_category():
    client = APIClient()
    payload = {"name": "Electronics"}
    response = client.post("/api/categories/", payload, format="json")

    assert response.status_code == 201
    assert Category.objects.count() == 1
    assert Category.objects.first().name == "Electronics"


