import pytest
from django.db import IntegrityError
from shop.models import Category, Product


@pytest.mark.django_db
def test_category_str_and_uniqueness():
    c1 = Category.objects.create(name="Electronics", slug="electronics")
    assert str(c1) == "Electronics"

    with pytest.raises(IntegrityError):
        Category.objects.create(name="Electronics", slug="electronics")


@pytest.mark.django_db
def test_product_creation_and_indexes():
    cat = Category.objects.create(name="Books", slug="books")
    p = Product.objects.create(
        category=cat,
        name="Django Unchained",
        slug="django-unchained",
        description="",
        price_cents=2599,
        currency="USD",
        is_active=True,
        stock=5,
    )
    assert p.id is not None
    assert p.category_id == cat.id

