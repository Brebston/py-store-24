from django.urls import path

from catalog.views import CatalogView, ProductDetailView

app_name = "catalog"

urlpatterns = [
    path("products/", CatalogView.as_view(), name="products"),
    path("product/<str:slug>/", ProductDetailView.as_view(), name="product"),
]
