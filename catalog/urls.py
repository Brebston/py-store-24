from django.urls import path

from catalog.views import CatalogView


app_name = "catalog"

urlpatterns = [
    path("products/", CatalogView.as_view(), name="products")
]
