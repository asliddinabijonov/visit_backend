from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "USER", "Oddiy foydalanuvchi"
        HOTEL_OWNER = "HOTEL_OWNER", "Mehmonxona egasi"
        RESTAURANT_OWNER = "RESTAURANT_OWNER", "Restoran egasi"
        TAXI_OWNER = "TAXI_OWNER", "Taxi"
        GUIDE = "GUIDE", "Gid"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    def __str__(self):
        return self.username

# Create your models here.
