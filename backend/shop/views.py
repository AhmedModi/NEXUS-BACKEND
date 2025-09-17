from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related(
        Prefetch('products', queryset=Product.objects.only('id', 'name', 'price_cents', 'is_active'))
    ).all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "created_at", "updated_at"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = (
        Product.objects.select_related("category")
        .only(
            "id",
            "category__id",
            "category__name",
            "name",
            "slug",
            "price_cents",
            "currency",
            "is_active",
            "stock",
            "created_at",
            "updated_at",
        )
        .all()
    )
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {"category": ["exact"], "is_active": ["exact"], "price_cents": ["gte", "lte"]}
    search_fields = ["name", "slug", "description"]
    ordering_fields = ["created_at", "price_cents", "name", "stock"]

from django.shortcuts import render

# Create your views here.
