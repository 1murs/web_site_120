from django.contrib import admin
from .models import Tire


# Register your models here.
@admin.register(Tire)
class TireAdmin(admin.ModelAdmin):
    list_display = ["brand", "model", "season", "width", "price", "quantity"]
    list_filter = ["brand", "season", "tire_type", "category"]
    search_fields = ["brand", "model", "article"]
    readonly_fields = ["slug", "created_at"]
    fieldsets = (
        (
            "Основна інформація",
            {"fields": ("brand", "model", "category", "description")},
        ),
        (
            "Характеристики",
            {"fields": ("width", "profile", "diameter", "tire_type", "season")},
        ),
        ("Індекси", {"fields": ("load_index", "speed_index")}),
        ("Комерційна інформація", {"fields": ("price", "article", "quantity")}),
        ("Зображення", {"fields": ("image",)}),
    )
