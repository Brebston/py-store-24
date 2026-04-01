from rest_framework import serializers

from catalog.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_active",
        )


class ProductSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "short_description",
            "description",
            "price",
            "stock",
            "image",
            "category",
            "highlights",
            "included",
            "specs",
            "is_active",
            "created_at",
        )
