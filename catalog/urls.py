from django.urls import include, path
from rest_framework import routers

from catalog.views import (
    ProductViewSet,
    CatalogView,
    ProductDetailView,
)

app_name = "catalog"

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("products/", CatalogView.as_view(), name="products"),
    path("products/<str:slug>/", ProductDetailView.as_view(), name="product"),
    path("api/", include(router.urls)),
]
