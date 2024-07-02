from django.core import validators
from django.db import models

from main_app.managers import DirectorManager


# Create your models here.


class Director(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            validators.MinLengthValidator(2),
            validators.MaxLengthValidator(120),
        ],
    )

    birth_date = models.DateField(
        default='1900-01-01',
    )

    nationality = models.CharField(
        max_length=50,
        validators=[
            validators.MaxLengthValidator(50),
        ],
        default='Unknown',
    )

    years_of_experience = models.SmallIntegerField(
        validators=[
            validators.MinValueValidator(0),
        ],
        default=0,
    )

    objects = DirectorManager()


class Actor(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            validators.MinLengthValidator(2),
            validators.MaxLengthValidator(120),
        ],
    )

    birth_date = models.DateField(
        default='1900-01-01',
    )

    nationality = models.CharField(
        max_length=50,
        validators=[
            validators.MaxLengthValidator(50),
        ],
        default='Unknown',
    )

    is_awarded = models.BooleanField(
        default=False,
    )

    last_updated = models.DateTimeField(
        auto_now=True,
    )


class Movie(models.Model):
    CHOICES_GENRE = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other'),
    ]

    title = models.CharField(
        max_length=150,
        validators=[
            validators.MinLengthValidator(5),
            validators.MaxLengthValidator(150),
        ],
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        validators=[
            validators.MaxLengthValidator(6),
        ],
        default='Other',
        choices=CHOICES_GENRE
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            validators.MinValueValidator(0.0),
            validators.MaxValueValidator(10.0)
        ],
        default=0.0,
    )

    is_classic = models.BooleanField(
        default=False,
    )

    is_awarded = models.BooleanField(
        default=False,
    )

    last_updated = models.DateTimeField(
        auto_now=True,
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,

    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='movies',
    )

