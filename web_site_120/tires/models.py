from django.db import models
from django.utils.text import slugify
from categories.models import Category


class Tire(models.Model):
    # Season
    SEASON_CHOICES = [
        ("summer", "Літня"),
        ("winter", "Зимова"),
        ("all_season", "Всесезонна"),
    ]

    # Type Tire
    TIRE_TYPE_CHOICES = [
        ("passenger", "Легковий"),
        ("truck", "Вантажний"),
        ("sport", "Спортивна"),
    ]

    # link to category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # General information
    brand = models.CharField(max_length=100)  # Brand (PETRO CYBER TRACK, ...)
    model = models.CharField(max_length=100)  # Model (122, Murs)

    # Tire specifications
    width = models.IntegerField()  # Width (185, 205 ...)
    profile = models.IntegerField()  # Profile (60, 234 ...)
    diameter = models.IntegerField()  # Diameter (14, 16, 17 ...)
    tire_type = models.CharField(max_length=50, choices=TIRE_TYPE_CHOICES)  # Type Tire
    season = models.CharField(max_length=50, choices=SEASON_CHOICES)  # Season
    load_index = models.IntegerField()  # Load index (82, 91...)
    speed_index = models.CharField(max_length=5)  # Speed index (H, V, W...)

    # Commercial information
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price(2145.00)
    article = models.CharField(max_length=50, unique=True)  # Article (1337)
    quantity = models.IntegerField()  # Quantity in stock

    # Picture and description
    image = models.ImageField(upload_to="tire_images/")
    description = models.TextField()

    # Date
    created_at = models.DateTimeField(auto_now_add=True)  # Date add

    slug = models.SlugField(unique=True, blank=True)

    # https://docs.djangoproject.com/en/5.2/topics/db/models/#overriding-predefined-model-methods
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.model}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} {self.width}/{self.profile}R{self.diameter}"

    class Meta:
        ordering = ["-created_at"]  # New Tires
        indexes = [
            models.Index(fields=["brand"]),
            models.Index(fields=["season"]),
            models.Index(fields=["slug"]),
        ]
        verbose_name = "Tier"
        verbose_name_plural = "Tires"
