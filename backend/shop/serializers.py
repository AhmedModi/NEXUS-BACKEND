from rest_framework import serializers
from .models import Category, Product
from django.utils.text import slugify
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_blank=True)
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "created_at", "updated_at"]

    def validate(self, attrs):
        name = attrs.get("name")
        slug = attrs.get("slug")
        if not slug and name:
            attrs["slug"] = slugify(name)
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    # expose decimal price in dollars; allow legacy price_cents input too
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, write_only=True)
    price_cents = serializers.IntegerField(required=False)
    price_out = serializers.DecimalField(source='price_cents', max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_id",
            "name",
            "slug",
            "description",
            "price",
            "price_out",
            "price_cents",
            "currency",
            "is_active",
            "stock",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # convert cents to decimal string under key 'price'
        cents = instance.price_cents if getattr(instance, 'price_cents', None) is not None else 0
        data['price'] = str(Decimal(cents) / Decimal(100))
        # remove internal helper
        data.pop('price_out', None)
        return data

    def validate(self, attrs):
        # normalize price fields: prefer 'price' if provided, else accept 'price_cents'
        price = attrs.pop('price', None)
        if price is not None:
            attrs['price_cents'] = int(Decimal(price) * 100)
        elif 'price_cents' in attrs and attrs['price_cents'] is not None:
            # keep as is
            pass
        else:
            raise serializers.ValidationError({"price": "Provide 'price' or 'price_cents'."})
        return attrs


