from django.db import models


class ShopSettings(models.Model):
    shipping_price = models.DecimalField(max_digits=6, decimal_places=2, default=4.00)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=8.00)

    def __str__(self):
        return "Shop Settings"
