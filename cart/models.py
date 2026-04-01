from django.conf import settings
from django.db import models
from django.db.models.constraints import UniqueConstraint

from catalog.models import Product
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user"], name="unique_cart_per_user"),
            UniqueConstraint(fields=["session_key"], name="unique_cart_per_session"),
        ]

    def __str__(self):
        if self.user_id:
            return f"Cart(user={self.user_id})"
        return f"Cart(session={self.session_key})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.select_related("product"))

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.select_related("product"))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["cart", "product"], name="unique_product_per_cart")
        ]

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def unit_price(self):
        return self.product.price

    @property
    def line_total(self):
        return self.product.price * self.quantity
