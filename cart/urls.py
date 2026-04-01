from django.urls import path

from cart.views import (
    CartClearAPIView,
    CartDetailAPIView,
    CartItemCreateAPIView,
    CartItemUpdateDeleteAPIView,
    CartPageView,
)

app_name = "cart"

urlpatterns = [
    path("", CartPageView.as_view(), name="page"),
    # API
    path("api/", CartDetailAPIView.as_view(), name="detail"),
    path("api/items/", CartItemCreateAPIView.as_view(), name="add-item"),
    path(
        "api/items/<int:item_id>/",
        CartItemUpdateDeleteAPIView.as_view(),
        name="item-update-delete",
    ),
    path("api/clear/", CartClearAPIView.as_view(), name="clear"),
]
