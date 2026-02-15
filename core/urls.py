from django.urls import path

from core.views import IndexView, ContactView, ReturnsView, ShippingView

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("returns/", ReturnsView.as_view(), name="returns"),
    path("shipping/", ShippingView.as_view(), name="shipping"),
]
