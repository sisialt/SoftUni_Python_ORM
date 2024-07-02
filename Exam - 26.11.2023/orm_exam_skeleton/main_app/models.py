from django.core import validators
from django.db import models

from orm_exam_skeleton.main_app.managers import AuthorManager


# Create your models here.


class ContentPublishedModel(models.Model):
    content = models.TextField(
        validators=[
            validators.MinLengthValidator(10)
        ]
    )

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        abstract = True


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(3)
        ],
    )

    email = models.EmailField(unique=True)

    is_banned = models.BooleanField(default=False)

    birth_year = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1900),
            validators.MaxValueValidator(2005)
        ],
    )

    website = models.URLField(null=True, blank=True)

    objects = AuthorManager()


class Article(ContentPublishedModel):
    CATEGORY_CHOICES = [
        ("Technology", "Technology"),
        ("Science", "Science"),
        ("Education", "Education"),
    ]

    title = models.CharField(
        max_length=200,
        validators=[
            validators.MinLengthValidator(5)
        ]
    )

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default="Technology",
    )

    authors = models.ManyToManyField(
        to=Author,
        related_name='articles',
    )


class Review(ContentPublishedModel):
    rating = models.FloatField(
        validators=[
            validators.MinValueValidator(1.0),
            validators.MaxValueValidator(5.0)
        ]
    )

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
