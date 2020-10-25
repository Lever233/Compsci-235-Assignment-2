from typing import List, Iterable

from Movie.adapters.repository import AbstractRepository
from Movie.domain.domain_model import make_comment, Movie, Review, Genre,Actor,Director


class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(article_id: int, comment_text: str, username: str, repo: AbstractRepository):
    # Check that the article exists.
    article = repo.get_movie(article_id)
    if article is None:
        raise NonExistentArticleException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_comment(comment_text, user, article)

    # Update the repository.
    repo.add_review(comment)


def get_movie(article_id: int, repo: AbstractRepository):
    article = repo.get_movie(article_id)

    if article is None:
        raise NonExistentArticleException

    return article_to_dict(article)


def get_first_movie(repo: AbstractRepository):

    article = repo.get_first_movie()

    return article_to_dict(article)


def get_last_movie(repo: AbstractRepository):

    article = repo.get_last_movie()
    return article_to_dict(article)


def get_movies_by_year(date, repo: AbstractRepository):
    # Returns articles for the target date (empty if no matches), the date of the previous article (might be null), the date of the next article (might be null)

    articles = repo.get_movie_by_year(target_date=date)

    articles_dto = list()
    prev_date = next_date = None

    if len(articles) > 0:

        # Convert Articles to dictionary form.
        articles_dto = articles_to_dict(articles)

    return articles_dto,prev_date,next_date


def get_movie_ranks_for_genre(tag_name, repo: AbstractRepository):
    article_ids = repo.get_movie_ranks_for_genre(tag_name)

    return article_ids


def get_movie_ranks_for_actor(actor_name,repo: AbstractRepository):
    movie_ids = repo.get_movie_ranks_for_actor(actor_name)

    return movie_ids


def get_movie_ranks_for_director(director_name, repo:AbstractRepository):
    movie_ids = repo.get_movie_ranks_for_director(director_name)
    return movie_ids


def get_movies_by_rank(id_list, repo: AbstractRepository):
    articles = repo.get_movie_by_rank(id_list)

    # Convert Articles to dictionary form.
    articles_as_dict = articles_to_dict(articles)

    return articles_as_dict


def get_comments_for_article(article_id, repo: AbstractRepository):
    article = repo.get_movie(article_id)

    if article is None:
        raise NonExistentArticleException

    return reviews_to_dict(article.review)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def article_to_dict(article: Movie):
    article_dict = {
        'release_year': article.release_year,
        'title': article.title,
        'description': article.description,
        'comments': reviews_to_dict(article.review),
        'tags': tags_to_dict(article.genres),
        'id': article.id
    }
    return article_dict


def articles_to_dict(articles: Iterable[Movie]):
    return [article_to_dict(article) for article in articles]


def review_to_dict(comment: Review):
    comment_dict = {
        'username': comment.user.user_name,
        'article_id': comment.movie.id,
        'comment_text': comment.review_text,
        "rating": comment.rating
    }
    return comment_dict


def reviews_to_dict(comments: Iterable[Review]):
    return [review_to_dict(comment) for comment in comments]


def genre_to_dict(tag: Genre):
    tag_dict = {
        'name': tag.genre_name,
        'tagged_articles': [article.id for article in tag.genre_movie]
    }
    return tag_dict


def tags_to_dict(tags: Iterable[Genre]):
    return [genre_to_dict(tag) for tag in tags]


def actor_to_dict(actor: Actor):
    actor_dict = {
        "name": actor.actor_full_name,
        "acted_movies": [movie.id for movie in actor.actor_movie]
    }
    return actor_dict


def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]


def director_to_dict(director: Director):
    director_dict = {
        "name": director.director_full_name,
        "directed_movie": [movie.id for movie in director.director_movie]
    }

    return director_dict


def directors_to_dict(directors: Iterable[Director]):
    return [director_to_dict(director) for director in directors]

# ============================================
# Functions to convert dicts to model entities
# ============================================


def dict_to_article(dict):
    article = Movie(dict.title, dict.release_year)
    # Note there's no comments or tags.
    return article