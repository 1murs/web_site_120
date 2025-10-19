from django.db import models
from users.models import User
from tires.models import Tire
from disks.models import Disk


class Order(models.Model):
    # Choices status
    STATUS_CHOICES = [
        ("new", "Нове"),
        ("paid", "Оплачено"),
        ("shipped", "Відправлено"),
        ("delivered", "Доставлено"),
        ("cancelled", "Скасовано"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Information about order
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.first_name} - {self.status}"

    class Meta:
        ordering = ["-created_at"]  # Новіші першими
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    # Link to the product (can be a tire or wheel)
    tire = models.ForeignKey(Tire, on_delete=models.SET_NULL, null=True, blank=True)
    disk = models.ForeignKey(Disk, on_delete=models.SET_NULL, null=True, blank=True)

    # Count and price
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price 1 product

    def get_total_price(self):
        """Calculates the total cost of goods in the order"""
        return self.quantity * self.price

    def get_product_name(self):
        """Returns the name of the product (tire or wheel)"""
        if self.tire:
            return f"{self.tire.brand} {self.tire.model}"
        if self.disk:
            return f"{self.disk.brand} {self.disk.model}"
        return "Unknown Product"

    def __str__(self):
        return f"Order #{self.order.id} - {self.get_product_name()} x{self.quantity}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
