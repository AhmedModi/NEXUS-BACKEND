import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from shop.models import Category, Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category():
    return Category.objects.create(name="Electronics", slug="electronics")


@pytest.mark.django_db
def test_list_products_empty(api_client):
    resp = api_client.get("/api/products/")
    assert resp.status_code == 200
    assert resp.json()["count"] == 0


@pytest.mark.django_db
def test_create_product_requires_auth(api_client, category):
    payload = {
        "category_id": category.id,
        "name": "Phone",
        "slug": "phone",
        "price_cents": 9999,
        "currency": "USD",
        "is_active": True,
        "stock": 10,
    }
    resp = api_client.post("/api/products/", payload, format="json")
    assert resp.status_code in (401, 403)


@pytest.mark.django_db
def test_create_update_delete_product_with_auth(api_client, category):
    user = User.objects.create_user(username="u1", password="pass12345")
    api_client.force_authenticate(user=user)

    payload = {
        "category_id": category.id,
        "name": "Phone",
        "slug": "phone",
        "price_cents": 9999,
        "currency": "USD",
        "is_active": True,
        "stock": 10,
    }
    resp = api_client.post("/api/products/", payload, format="json")
    assert resp.status_code == 201
    pid = resp.json()["id"]

    # Update
    resp = api_client.patch(f"/api/products/{pid}/", {"price_cents": 8999}, format="json")
    assert resp.status_code == 200
    assert resp.json()["price_cents"] == 8999

    # Delete
    resp = api_client.delete(f"/api/products/{pid}/")
    assert resp.status_code == 204


@pytest.mark.django_db
def test_products_filtering_and_search(api_client, category):
    other = Category.objects.create(name="Books", slug="books")
    Product.objects.create(category=category, name="iPhone", slug="iphone", price_cents=10000, currency="USD", is_active=True, stock=5)
    Product.objects.create(category=category, name="Old Phone", slug="old-phone", price_cents=1000, currency="USD", is_active=False, stock=1)
    Product.objects.create(category=other, name="Python Book", slug="python-book", price_cents=2000, currency="USD", is_active=True, stock=10)

    # Filter by category
    resp = api_client.get(f"/api/products/?category={category.id}")
    assert resp.status_code == 200
    names = [r["name"] for r in resp.json()["results"]]
    assert set(names) == {"iPhone", "Old Phone"}

    # Filter by is_active
    resp = api_client.get("/api/products/?is_active=true")
    names = [r["name"] for r in resp.json()["results"]]
    assert set(names) == {"iPhone", "Python Book"}

    # Price range
    resp = api_client.get("/api/products/?price_cents__gte=1500&price_cents__lte=12000")
    names = [r["name"] for r in resp.json()["results"]]
    assert set(names) == {"iPhone", "Python Book"}

    # Search
    resp = api_client.get("/api/products/?search=phone")
    names = [r["name"] for r in resp.json()["results"]]
    assert set(names) == {"iPhone", "Old Phone"}


