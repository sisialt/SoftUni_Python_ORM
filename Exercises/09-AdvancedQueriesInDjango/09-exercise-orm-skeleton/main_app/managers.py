from _decimal import Decimal
from django.db import models
from django.db.models import QuerySet, Count, Max, Min, Avg


class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str) -> QuerySet:
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet:
        return self.filter(price__range=(min_price, max_price))

    def with_bedrooms(self, bedrooms_count: int) -> QuerySet:
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self) -> QuerySet:
        most_visited = self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'id')[:2]

        return most_visited


class VideoGameManager(models.Manager):
    def games_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        return self.annotate(max_rated=Max('rating')).order_by('-max_rated')[0]

    def lowest_rated_game(self):
        return self.annotate(min_rated=Min('rating')).order_by('min_rated')[0]

    def average_rating(self):
        average_rating = self.aggregate(average_rating=Avg('rating'))["average_rating"]
        return f"{average_rating:.1f}"












