from django.shortcuts import render
from django.views.generic import DetailView, ListView

from catalog.models import Product


class CatalogView(ListView):
    model = Product
    template_name = "catalog/products.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"