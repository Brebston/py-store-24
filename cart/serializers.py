from rest_framework import serializers
from cart.models import Cart, CartItem
from catalog.models import Product
from catalog.serializers import ProductSerializer
from core.models import ShopSettings


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "slug", "name", "price")


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    line_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "unit_price", "line_total")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        settings = ShopSettings.objects.first()

        shipping = settings.shipping_price
        tax = instance.subtotal * (settings.tax_percent / 100)

        data["shipping"] = shipping
        data["tax"] = tax
        data["total"] = instance.subtotal + shipping + tax

        return data

    class Meta:
        model = Cart
        fields = ("id", "items", "total_items", "subtotal")


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=False)
    product_slug = serializers.CharField(required=False)
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, attrs):
        product_id = attrs.get("product_id")
        product_slug = attrs.get("product_slug")

        if not product_id and not product_slug:
            raise serializers.ValidationError("Pass the product_id or product_slug.")

        if product_id:
            product = Product.objects.filter(id=product_id).first()
        else:
            product = Product.objects.filter(slug=product_slug).first()

        if not product:
            raise serializers.ValidationError("Product not found.")

        attrs["product"] = product
        return attrs


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)
