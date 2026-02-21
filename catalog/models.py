import pathlib
import uuid

from django.db import models
from django.template.defaultfilters import slugify


def product_image_path(
        instance: "Product",
        filename: str
) -> pathlib.Path:
    filename = (f"{slugify(instance.name)}-{uuid.uuid4()}"
                + pathlib.Path(filename).suffix)
    return pathlib.Path("uploads/products/") / pathlib.Path(filename)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(null=True, upload_to=product_image_path)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.stock}"

    @property
    def product_stock(self):
        if self.stock <= 0:
            return "Sold Out"
        elif self.stock <= 10:
            return "Low Stock"
        return "In Stock"

