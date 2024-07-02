from django.core import validators
from django.db import models

from main_app.managers import ProfileManager
from main_app.mixins import TimeStampMixin


class Profile(TimeStampMixin):
    full_name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(2),
        ],
    )

    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15,
    )

    address = models.TextField()

    is_active = models.BooleanField(
        default=True,
    )

    objects = ProfileManager()

    def __str__(self):
        return f"{self.full_name}"


class Product(TimeStampMixin):
    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0.01)
        ],
    )

    in_stock = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(0)
        ],
    )

    is_available = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f"{self.name}"


class Order(TimeStampMixin):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='orders',
    )

    products = models.ManyToManyField(
        to=Product,
        related_name='orders',
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0.01)
        ],
    )

    is_completed = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.profile} {self.total_price}"

