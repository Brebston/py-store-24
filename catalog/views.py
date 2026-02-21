from django.shortcuts import render
from django.views.generic import ListView

from catalog.models import Product


class CatalogView(ListView):
    model = Product
    template_name = "catalog/products.html"