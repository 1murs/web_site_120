from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of category (disks, tires)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    # https://docs.djangoproject.com/en/5.2/topics/db/models/#overriding-predefined-model-methods
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),  
        ]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
