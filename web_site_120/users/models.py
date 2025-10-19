from django.db import models


class User(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
