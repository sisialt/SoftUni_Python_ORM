import os
import django
from django.db.models import Count, Avg, F, Q

from populate_db import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Movie, Actor


def get_directors(search_name=None, search_nationality=None):
    result = []
    if search_name is None and search_nationality is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name and search_nationality:
        query = query_name & query_nationality
    elif search_name:
        query = query_name
    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    for director in directors:
        result.append(f"Director: {director.full_name}, "
                      f"nationality: {director.nationality}, "
                      f"experience: {director.years_of_experience}")
    return '\n'.join(result)

    # if search_name is None:
    #     directors = Director.objects.filter(nationality__icontains=search_nationality).order_by('full_name')
    #     if not directors:
    #         return ""
    #     for director in directors:
    #         result.append(f"Director: {director.full_name}, "
    #                       f"nationality: {director.nationality}, "
    #                       f"experience: {director.years_of_experience}")
    #     return '\n'.join(result)
    #
    # if search_nationality is None:
    #     directors = Director.objects.filter(full_name__icontains=search_name).order_by('full_name')
    #     if not directors:
    #         return ""
    #     for director in directors:
    #         result.append(f"Director: {director.full_name}, "
    #                       f"nationality: {director.nationality}, "
    #                       f"experience: {director.years_of_experience}")
    #     return '\n'.join(result)
    #
    # directors = (Director.objects.filter(full_name__icontains=search_name, nationality__icontains=search_nationality)
    #              .order_by('full_name'))
    # if not directors:
    #     return ""
    # for director in directors:
    #     result.append(f"Director: {director.full_name}, "
    #                   f"nationality: {director.nationality}, "
    #                   f"experience: {director.years_of_experience}")
    # return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()
    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.num_movies}."


def get_top_actor():
    if not Movie.objects.all() or not Movie.objects.exclude(starring_actor__isnull=True):
        return ""

    top_actor = Actor.objects.annotate(num_movies=Count('movie')).order_by('-num_movies', 'full_name').first()
    movies = top_actor.movie_set.all()
    avg_rating = movies.aggregate(av_rat=Avg('rating'))['av_rat']

    return (f"Top Actor: {top_actor.full_name}, "
            f"starring in movies: {', '.join([m.title for m in movies])}, "
            f"movies average rating: {avg_rating:.1f}")


def get_actors_by_movies_count():
    movies = Movie.objects.all()
    if not movies or not movies.exclude(actors__isnull=True):
        return ""

    result = []
    actors = Actor.objects.annotate(num_movies=Count('movies')
                                    ).exclude(num_movies=0
                                              ).order_by('-num_movies', 'full_name')[:3]

    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    top_rated_movie = Movie.objects.filter(is_awarded=True
                                           ).order_by('-rating', 'title').first()
    # add .select_related('starring_actor').prefetch_related('actors')

    if not top_rated_movie:  # forgot
        return ""

    return (f"Top rated awarded movie: {top_rated_movie.title}, "
            f"rating: {top_rated_movie.rating:.1f}. "
            f"Starring actor: "
            f"{top_rated_movie.starring_actor.full_name if top_rated_movie.starring_actor is not None else 'N/A'}. "
            f"Cast: {', '.join([a.full_name for a in top_rated_movie.actors.order_by('full_name')])}.")


def increase_rating():
    classic_movies = Movie.objects.filter(is_classic=True, rating__lt=9.9)
    if not classic_movies:
        return "No ratings increased."

    classic_movies.update(rating=F('rating') + 0.1)

    return f"Rating increased for {classic_movies.count()} movies."

# director = Director.objects.get(pk=4)
# movie = Movie.objects.first()
# print(movie.director)
# print(director.movie_set.all())
# actor = Actor.objects.create(
#     full_name='Sis',
#
# )
# movie = Movie.objects.create(
#     title='movie',
#     release_date='2023-08-01',
#     director=Director.objects.all().first(),
#     starring_actor=Actor.objects.all().first(),
#
# )
# print(get_top_actor())

# actor = Actor.objects.get(pk=5)
# actor.movies.add(Movie.objects.get(pk=2), Movie.objects.get(pk=3))
# print(get_actors_by_movies_count())
# movie = Movie.objects.get(pk=5)
# movie.is_awarded = True
# print(get_top_rated_awarded_movie())
# print(increase_rating())
# print(Director.objects.get_directors_by_movies_count())
# print(Director.objects.first().movie_set.all())

populate_model_with_data(Movie)