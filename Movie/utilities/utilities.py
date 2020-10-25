from flask import Blueprint, request, render_template, redirect, url_for, session

import Movie.adapters.repository as repo
import Movie.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_tags_and_urls():
    tag_names = services.get_genre_names(repo.repo_instance)
    tag_urls = dict()
    for tag_name in tag_names:
        tag_urls[tag_name] = url_for('news_bp.articles_by_genre', tag=tag_name)

    return tag_urls


def get_actors_and_urls():
    actor_names = services.get_actor_name(repo.repo_instance)
    actor_urls = dict()
    for actor_name in actor_names:
        actor_urls[actor_name] = url_for("news_bp.movie_by_actor", actor = actor_name)

    return actor_urls
def get_director_and_url():
    director_names = services.get_director_name(repo.repo_instance)
    director_urls = dict()
    for director_name in director_names:
        director_urls[director_name] = url_for("news.bp.movies_by_director", director = director_name)

    return director_urls

def get_selected_articles(quantity=3):
    articles = services.get_random_articles(quantity, repo.repo_instance)

    for article in articles:
        article['hyperlink'] = url_for('news_bp.articles_by_date', date=article['date'])
    return articles