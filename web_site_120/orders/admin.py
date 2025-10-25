from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total_price", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__first_name", "user__last_name"]
    inlines = [OrderItemInline]
    readonly_fields = ["created_at", "updated_at"]


admin.site.register(OrderItem)
