from django.contrib import admin

from core.models import ShopSettings


@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    pass
