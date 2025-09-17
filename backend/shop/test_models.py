import pytest
from shop.models import Category

@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Electronics")
    assert category.name == "Electronics"
    assert Category.objects.count() == 1
