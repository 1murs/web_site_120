from django.contrib import admin
from .models import Disk


@admin.register(Disk)
class DiskAdmin(admin.ModelAdmin):
    list_display = ["brand", "model", "diameter", "price", "quantity", "created_at"]
    list_filter = ["brand", "diameter", "category"]
    search_fields = ["brand", "model", "article"]
    readonly_fields = ["slug", "created_at"]
    fieldsets = (
        (
            "Основна інформація",
            {"fields": ("brand", "model", "category", "description")},
        ),
        ("Характеристики", {"fields": ("diameter", "width", "pcd", "dia")}),
        ("Комерційна інформація", {"fields": ("price", "article", "quantity")}),
        ("Зображення", {"fields": ("image",)}),
        ("Служебна", {"fields": ("slug", "created_at"), "classes": ("collapse",)}),
    )
