from flask import Blueprint, render_template

import Movie.utilities.utilities as utilities


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        selected_articles=utilities.get_selected_articles(),
        tag_urls=utilities.get_tags_and_urls(),
        actor_urls=utilities.get_actors_and_urls()
    )
