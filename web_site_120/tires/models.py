from django.db import models
from django.utils.text import slugify
from categories.models import Category


class TireQuerySet(models.QuerySet):
    """Custom methods for tire search"""

    def search(self, query):
        return self.filter(
            models.Q(brand__icontains=query)
            | models.Q(model__icontains=query)
            | models.Q(article__icontains=query)
        )

    def by_brand(self, brand):
        """Filter by brand"""
        return self.filter(brand=brand)

    def by_season(self, season):
        """Filter by season"""
        return self.filter(season=season)

    def by_price_range(self, min_price, max_price):
        """Filter by price"""
        return self.filter(price__gte=min_price, price__lte=max_price)

    def by_diameter(self, diameter):
        """Filter by diameter"""
        return self.filter(diameter=diameter)

    def in_stock(self):
        """Only products in stock"""
        return self.filter(quantity__gt=0)


class TireManager(models.Manager):
    def get_queryset(self):
        return TireQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    def by_brand(self, brand):
        return self.get_queryset().by_brand(brand)

    def by_season(self, season):
        return self.get_queryset().by_season(season)

    def by_diameter(self, diameter):
        return self.get_queryset().by_diameter(diameter)

    def by_price_range(self, min_price, max_price):
        return self.get_queryset().by_price_range(min_price, max_price)

    def in_stock(self):
        return self.get_queryset().in_stock()


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

    objects = TireManager()

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
