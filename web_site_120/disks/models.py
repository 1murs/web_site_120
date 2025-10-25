from django.db import models
from django.utils.text import slugify
from categories.models import Category


class DiskQuerySet(models.QuerySet):
    """Custom method for search Disks"""

    def search(self, query):
        """Search by brand, model, article"""
        return self.filter(
            models.Q(brand__icontains=query)
            | models.Q(model__icontains=query)
            | models.Q(article__icontains=query)
        )

    def by_brand(self, brand):
        """Filter by brand"""
        return self.filter(brand=brand)

    def by_diameter(self, diameter):
        """Filter by diameter"""
        return self.filter(diameter=diameter)

    def by_price_range(self, min_price, max_price):
        """Filter by price"""
        return self.filter(price__gte=min_price, price__lte=max_price)

    def in_stock(self):
        """Only products in stock"""
        return self.filter(quantity__gt=0)


class DiskManager(models.Manager):
    def get_queryset(self):
        return DiskQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    def by_brand(self, brand):
        return self.get_queryset().by_brand(brand)

    def by_diameter(self, diameter):
        return self.get_queryset().by_diameter(diameter)

    def by_price_range(self, min_price, max_price):
        return self.get_queryset().by_price_range(min_price, max_price)

    def in_stock(self):
        return self.get_queryset().in_stock()


class Disk(models.Model):
    # link to category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # General information
    brand = models.CharField(max_length=100)  # Manufacturer (AEZ, Borbet...)
    model = models.CharField(max_length=100)  # Model (AIRBLADE, Alpha...)

    # Drive specifications
    diameter = models.IntegerField()  # Diameter (17, 18, 19...)
    width = models.IntegerField()  # Disc width (8, 9, 10...)
    pcd = models.CharField(max_length=20)  # PCD (5X112, 5X120...)
    dia = models.DecimalField(max_digits=5, decimal_places=1)  #  DIA (70.1, 72.6...

    # Commercial information
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price
    article = models.CharField(max_length=50, unique=True)  # Article (13123...)
    quantity = models.IntegerField()  # Quantity in stock

    # Picture and description
    image = models.ImageField(upload_to="disk_images/")
    description = models.TextField()

    # Date
    created_at = models.DateTimeField(auto_now_add=True)  # Date

    slug = models.SlugField(unique=True, blank=True)

    objects = DiskManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.model}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} {self.diameter}x{self.width} {self.pcd}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["brand"]),
            models.Index(fields=["diameter"]),
            models.Index(fields=["slug"]),
        ]
        verbose_name = "Disk"
        verbose_name_plural = "Disks"
