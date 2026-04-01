from cart.serializers import (
    AddToCartSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)
from cart.services import (
    add_product_to_cart,
    clear_cart,
    get_cart,
    update_cart_item_quantity,
)
from cart.models import CartItem

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class CartPageView(TemplateView):
    template_name = "cart/cart.html"


class CartDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart = get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_cart(request)
        try:
            item = add_product_to_cart(
                cart=cart,
                product=serializer.validated_data["product"],
                quantity=serializer.validated_data["quantity"],
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(
            {
                "message": "The item has been added to your basket.",
                "item_id": item.id,
                "cart": CartSerializer(cart).data,
            },
            status=status.HTTP_201_CREATED,
        )


class CartItemUpdateDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, item_id):
        cart = get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            updated_item = update_cart_item_quantity(
                item=item, quantity=serializer.validated_data["quantity"]
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(
            {
                "message": "Cart updated.",
                "deleted": updated_item is None,
                "cart": CartSerializer(cart).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, item_id):
        cart = get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        item.delete()

        return Response({"message": "Item removed.", "cart": CartSerializer(cart).data})


class CartClearAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        cart = get_cart(request)
        clear_cart(cart)

        return Response(
            {
                "message": "Your basket has been cleared.",
                "cart": CartSerializer(cart).data,
            }
        )


def cart_page(request):
    return render(request, "cart/cart.html")
