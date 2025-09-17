from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    slug = models.SlugField(max_length=140, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"], name="category_name_idx"),
            models.Index(fields=["slug"], name="category_slug_idx"),
        ]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    description = models.TextField(blank=True)
    price_cents = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default="USD")
    is_active = models.BooleanField(default=True, db_index=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"], name="product_name_idx"),
            models.Index(fields=["is_active", "category"], name="product_active_category_idx"),
            models.Index(fields=["price_cents"], name="product_price_idx"),
        ]

    def __str__(self) -> str:
        return self.name


# Create your models here.
