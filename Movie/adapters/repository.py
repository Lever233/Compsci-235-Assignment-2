import abc
from typing import List
from datetime import date

from Movie.domain.domain_model import Movie, Genre, User, Review, make_genre_association, make_comment,Director,Actor


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie,rank: float,description:str):
        """ Adds an Article to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie (self, id: int) -> Movie:
        """ Returns Article with id from the repository.

        If there is no Article with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_year(self, target_date: int) -> List[Movie]:
        """ Returns a list of Articles that were published on target_date.

        If there are no Articles on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movie(self):
        """ Returns the number of Articles in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_rank(self, id_list):
        """ Returns a list of Articles, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ranks_for_genre(self, tag_name: str):
        """ Returns a list of ids representing Articles that are tagged by tag_name.

        If there are Articles that are tagged by tag_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ranks_for_actor(self,actor_name:str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ranks_for_director(self,director_name:str):
        raise NotImplementedError
    @abc.abstractmethod

    def add_genre(self, tag: Genre):
        """ Adds a Tag to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the Tags stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, comment: Review):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if comment.user is None or comment not in comment.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if comment.movie is None or comment not in comment.movie.review:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_directors(self):
        """ Return the Directors in the repository."""
        raise NotImplementedError
    @abc.abstractmethod
    def add_director(self,director:Director):
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors(self):
        raise NotImplementedError



