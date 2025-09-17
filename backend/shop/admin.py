from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price_cents", "is_active", "stock")
    list_filter = ("is_active", "category")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
from django.contrib import admin

# Register your models here.
