from datetime import date

from Movie.domain.domain_model import User, Actor, Genre, Review, Movie, Director, MovieFileCSVReader, ModelException, \
    make_comment, make_genre_association

import pytest


@pytest.fixture()
def movie():
    return Movie('Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room',2020)


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def genre():
    return Genre('New Zealand')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie>'

    for comment in user.reviews:
        # User should have an empty list of Comments after construction.
        assert False


def test_article_construction(movie):
    assert movie.id is None
    #assert movie.date == date.fromisoformat('2020-03-15')
    assert movie.title == 'Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room'
    #assert movie.first_para == 'The self-isolation deadline has been pushed back'
    #assert movie.hyperlink == 'https://www.nzherald.co.nz/business/news/article.cfm?c_id=3&objectid=12316800'
    #assert movie.image_hyperlink == 'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'

    assert movie.number_of_review == 0
    assert movie.number_of_genres == 0

    assert repr(
        movie) == '<Movie Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room, 2020>'


def test_article_less_than_operator():
    article_1 = Movie(
        "",2019
    )

    article_2 = Movie(
        "", 2020
    )

    assert article_1 < article_2


def test_tag_construction(genre):
    assert genre.genre_name == 'New Zealand'

    for movie in genre.genre_movie:
        assert False

    assert not genre.is_applied_to(Movie("", 1900))


def test_make_comment_establishes_relationships(movie, user):
    comment_text = 'COVID-19 in the USA!'
    comment = make_comment(comment_text, user, movie)

    # Check that the User object knows about the Comment.
    assert comment in user.reviews

    # Check that the Comment knows about the User.
    assert comment.user is user

    # Check that Article knows about the Comment.
    assert comment in movie.review

    # Check that the Comment knows about the Article.
    assert comment.movie is movie


def test_make_genre_associations(movie, genre):
    make_genre_association(movie, genre)

    # Check that the Article knows about the Tag.
    assert movie.is_genred()
    assert movie.is_genred_by(genre)

    # check that the Tag knows about the Article.
    assert genre.is_applied_to(movie)
    assert movie in genre.genre_movie


def test_make_tag_associations_with_article_already_tagged(movie, genre):
    make_genre_association(movie, genre)

    with pytest.raises(ModelException):
        make_genre_association(movie, genre)
