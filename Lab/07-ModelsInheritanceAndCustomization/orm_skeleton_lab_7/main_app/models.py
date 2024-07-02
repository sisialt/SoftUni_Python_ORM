from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = (
            (True, "Available"),
            (False, "Not Available")
        )
        kwargs['default'] = True
        super().__init__(*args, **kwargs)


class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        age = date.today().year - self.birth_date.year
        if (date.today().month < self.birth_date.month or
                (date.today().month == self.birth_date.month and date.today().day < self.birth_date.day)):
            age -= 1
        return age


class Mammal(Animal):
    fur_color = models.CharField(max_length=50)


class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class ZooKeeper(Employee):
    # class Specialties(models.TextChoices):
    #     Mammals = "Mammals"
    #     Birds = "Birds"
    #     Reptiles = "Reptiles"
    #     Others = "Others"

    SPECIALTY_CHOICES = [
        ("Mammals", "Mammals"),
        ("Birds", "Birds"),
        ("Reptiles", "Reptiles"),
        ("Others", "Others"),
    ]

    specialty = models.CharField(max_length=10, choices=SPECIALTY_CHOICES)
    # specialty = models.CharField(max_length=10, choices=Specialties.choices)
    managed_animals = models.ManyToManyField(to=Animal)

    def clean(self):
        super().clean()

        # if self.specialty not in self.Specialities:
        if self.specialty not in [sp[0] for sp in self.SPECIALTY_CHOICES]:
            raise ValidationError("Specialty must be a valid choice.")


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()

    def is_available(self):
        return self.availability


class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True

    def display_info(self):
        extra_info = ''
        if hasattr(self, "mammal"):
            extra_info = f" Its fur color is {self.mammal.fur_color}."
        elif hasattr(self, "bird"):
            extra_info = f" Its wingspan is {self.bird.wing_span} cm."
        elif hasattr(self, "reptile"):
            extra_info = f" Its scale type is {self.reptile.scale_type}."

        return (f"Meet {self.name}! It's {self.species} and it's born {self.birth_date}. "
                f"It makes a noise like '{self.sound}'!{extra_info}")

    def is_endangered(self):
        if self.species in ["Cross River Gorilla", "Orangutan", "Green Turtle"]:
            return True
        return False


