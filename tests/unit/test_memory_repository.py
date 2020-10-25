from datetime import date, datetime
from typing import List

import pytest

from Movie.domain.domain_model import User, Movie, Genre, Review, make_comment
from Movie.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')



def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_article_count(in_memory_repo):
    number_of_articles = in_memory_repo.get_number_of_movie()

    # Check that the query returned 6 Articles.
    assert number_of_articles == 5


def test_repository_can_add_article(in_memory_repo):
    article = Movie(
        'Second US coronavirus cruise tests negative amid delays and cancellations',2019
    )
    in_memory_repo.add_movie(article,3,"blahbalah")

    assert in_memory_repo.get_movie(3) is article


def test_repository_can_retrieve_article(in_memory_repo):
    article = in_memory_repo.get_movie(1)

    # Check that the Article has the expected title.
    assert article.title == 'Guardians of the Galaxy'

    # Check that the Article is commented as expected.
    comment_one = [comment for comment in article.review if comment.review_text == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    comment_two = [comment for comment in article.review if comment.review_text == 'Yeah Freddie, bad news'][0]

    assert comment_one.user.user_name == 'fmercury'
    assert comment_two.user.user_name == "thorke"

    # Check that the Article is tagged as expected.
    assert article.is_genred_by(Genre('Action'))
    assert article.is_genred_by(Genre('Adventure'))


def test_repository_does_not_retrieve_a_non_existent_article(in_memory_repo):
    article = in_memory_repo.get_movie(101)
    assert article is None


def test_repository_can_retrieve_articles_by_date(in_memory_repo):
    articles = in_memory_repo.get_movie_by_year(2016)

    # Check that the query returned 3 Articles.
    assert len(articles) == 3




def test_repository_can_retrieve_tags(in_memory_repo):
    tags: List[Genre] = in_memory_repo.get_genres()

    assert len(tags) == 10

    tag_one = [tag for tag in tags if tag.genre_name == 'Action'][0]
    tag_two = [tag for tag in tags if tag.genre_name == 'Adventure'][0]
    tag_three = [tag for tag in tags if tag.genre_name == 'Sci-Fi'][0]
    tag_four = [tag for tag in tags if tag.genre_name == 'Mystery'][0]

    assert tag_one.number_of_genre_movie == 2
    assert tag_two.number_of_genre_movie == 3
    assert tag_three.number_of_genre_movie == 2
    assert tag_four.number_of_genre_movie == 1


def test_repository_can_get_first_article(in_memory_repo):
    article = in_memory_repo.get_first_movie()
    assert article.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_article(in_memory_repo):
    article = in_memory_repo.get_last_movie()
    assert article.title == 'Suicide Squad'


def test_repository_can_get_articles_by_ids(in_memory_repo):
    articles = in_memory_repo.get_movie_by_rank([1,2,3])

    assert len(articles) == 3
    assert articles[
               0].title == 'Guardians of the Galaxy'
    assert articles[1].title == "Prometheus"
    assert articles[2].title == 'Split'


def test_repository_does_not_retrieve_article_for_non_existent_id(in_memory_repo):
    articles = in_memory_repo.get_movie_by_rank([2, 9])

    assert len(articles) == 1
    assert articles[
               0].title == 'Prometheus'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    articles = in_memory_repo.get_movie_by_rank([0, 9])

    assert len(articles) == 0


def test_repository_returns_article_ids_for_existing_tag(in_memory_repo):
    article_ids = in_memory_repo.get_movie_ranks_for_genre('Adventure')

    assert article_ids == [1, 2, 5]


def test_repository_returns_an_empty_list_for_non_existent_tag(in_memory_repo):
    article_ids = in_memory_repo.get_movie_ranks_for_genre('United States')

    assert len(article_ids) == 0



def test_repository_can_add_a_tag(in_memory_repo):
    tag = Genre('Motoring')
    in_memory_repo.add_genre(tag)

    assert tag in in_memory_repo.get_genres()


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    article = in_memory_repo.get_movie(2)
    comment = make_comment("Trump's onto it!", user, article)

    in_memory_repo.add_review(comment)

    assert comment in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    article = in_memory_repo.get_movie(2)
    comment = Review(None, article, "Trump's onto it!",5)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(comment)


def test_repository_does_not_add_a_comment_without_an_article_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    article = in_memory_repo.get_movie(2)
    comment = Review(None, article, "Trump's onto it!",5)

    user.add_review(comment)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_review(comment)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 2



