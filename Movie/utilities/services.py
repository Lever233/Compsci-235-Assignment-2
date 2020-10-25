from typing import Iterable
import random

from Movie.adapters.repository import AbstractRepository
from Movie.domain.domain_model import Movie, Genre, User, Review, make_genre_association, make_comment,Director,Actor,make_actor_association,make_director_association



def get_genre_names(repo: AbstractRepository):
    tags = repo.get_genres()
    tag_names = [tag.genre_name for tag in tags]

    return tag_names


def get_actor_name(repo: AbstractRepository):
    actors = repo.get_actors()
    actor_names =[actor.actor_full_name for actor in actors]

    return actor_names


def get_director_name(repo:AbstractRepository):
    director = repo.get_directors()

    return director


def get_random_articles(quantity, repo: AbstractRepository):
    article_count = repo.get_number_of_movie()

    if quantity >= article_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = article_count - 1

    # Pick distinct and random articles.
    random_ids = random.sample(range(1, article_count), quantity)
    articles = repo.get_movie_by_rank(random_ids)

    return articles_to_dict(articles)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def article_to_dict(article: Movie):
    article_dict = {
        'date': article.release_year,
        'title': article.title,
        'first_para':article.description
    }
    return article_dict


def articles_to_dict(articles: Iterable[Movie]):
    return [article_to_dict(article) for article in articles]
