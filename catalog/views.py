from django.views.generic import DetailView, ListView

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from catalog.models import Product
from catalog.serializers import ProductSerializer


class CatalogView(ListView):
    model = Product
    template_name = "catalog/products.html"


class ProductViewSet(viewsets.ModelViewSet):
    """DRF ViewSet for Product model."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = []
        else:
            self.permission_classes = [IsAdminUser]
        return [permission() for permission in self.permission_classes]


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"