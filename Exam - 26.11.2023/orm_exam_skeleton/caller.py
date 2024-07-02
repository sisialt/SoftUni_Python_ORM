import os
import django

# from populate_db import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from django.db.models import Q, Count, Avg, Sum, Max
from main_app.models import Author, Article, Review


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name and search_email:
        query = query_name & query_email
    elif search_name:
        query = query_name
    else:
        query = query_email

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors:
        return ""

    result = []

    for a in authors:
        result.append(f"Author: {a.full_name}, "
                      f"email: {a.email}, "
                      f"status: {'Banned' if a.is_banned else 'Not Banned'}")

    return '\n'.join(result)


def get_top_publisher():
    top_author = Author.objects.get_authors_by_article_count().first()

    if not top_author or not top_author.num_articles:
        return ""

    return f"Top Author: {top_author.full_name} with {top_author.num_articles} published articles."


def get_top_reviewer():
    author = Author.objects.annotate(
        num_reviews=Count('reviews')
    ).order_by(
        '-num_reviews',
        'email'
    ).first()

    if not author or not author.num_reviews:
        return ""

    return f"Top Reviewer: {author.full_name} with {author.num_reviews} published reviews."


# def get_top_rated_article():
#     # top_article = Article.objects.annotate(
#     #     num_reviews=Count('reviews'),
#     #     avg_rating=Avg('reviews__rating')
#     # ).order_by(
#     #     '-reviews__rating',
#     #     'title'
#     # ).first()
#     top_article = Article.objects.values('reviews__rating').order_by('-reviews__rating').all()
#     top_article_average_rating = Article.objects.aggregate(av=Avg('reviews__rating'))
#
#     print(top_article.__dict__)
#     print(top_article_average_rating)
#
#     if not top_article: # or top_article.num_reviews == 0:
#         return ""
#
#     return (f"The top-rated article is: {top_article.title}, "
#             f"with an average rating of {top_article.avg_rating:.2f}, "
#             f"reviewed {top_article.reviews.count()} times.")


def ban_author(email=None):
    if email is None or not Author.objects.all() or not Author.objects.filter(email__exact=email).first():
        return "No authors banned."

    Author.objects.filter(email__exact=email).update(is_banned=True)
    author = Author.objects.filter(email__exact=email).first()
    num_deleted_reviews = author.reviews.all().delete()[0]
    author.save()

    return f"Author: {author.full_name} is banned! {num_deleted_reviews} reviews deleted."


# def get_top_rated_article():
#     article = (Article.objects.annotate(
#         num_reviews=Count('reviews')
#     ).filter(
#         num_reviews__gt=0
#     ).order_by(
#         '-reviews__rating',
#         'title'
#     ).first())
#
#     if not article.reviews:
#         return ""
#
#     if article.reviews.count() == 0:
#         avg_rating = 0
#     else:
#         avg_rating = Review.objects.filter(article_id=article.id).aggregate(
#             av=Avg('rating')
#         )['av']
#
#     return (f"The top-rated article is: {article.title}, "
#             f"with an average rating of {avg_rating:.2f}, "
#             f"reviewed {article.reviews.count()} times.")


def get_latest_article():
    if not Article.objects.all():
        return ""

    article = Article.objects.last()
    if article.reviews.count() == 0:
        avg_rating = 0
    else:
        avg_rating = Review.objects.filter(article_id=article.id).aggregate(
            av=Avg('rating')
        )['av']

    return (f"The latest article is: {article.title}. "
            f"Authors: {', '.join(a.full_name for a in article.authors.all())}. "
            f"Reviewed: {article.reviews.count()} times. "
            f"Average Rating: {avg_rating:.2f}.")


def get_top_rated_article():
    if not Review.objects.all():
        return ""

    top_review = Review.objects.order_by('-rating').first()
    article = Article.objects.filter(reviews__rating=top_review.rating).order_by('title').first()

    # article = (Article.objects.annotate(
    #     num_reviews=Count('reviews'),
    # ).filter(
    #     num_reviews__gt=0
    # ).order_by(
    #     '-reviews__rating',
    #     'title'
    # ).first())
    # # print(article.__dict__)

    if not article:
        return ""

    avg_rating = Review.objects.filter(article_id=article.id).aggregate(
            av=Avg('rating')
        )['av']

    return (f"The top-rated article is: {article.title}, "
            f"with an average rating of {avg_rating:.2f}, "
            f"reviewed {article.reviews.count()} times.")

# print(get_top_rated_article())
# print(get_latest_article())
