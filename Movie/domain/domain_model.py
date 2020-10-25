from datetime import datetime
from typing import List, Iterable

import csv



class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

        self.__director_movie: List[Movie] = list()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @property
    def director_movie(self) -> Iterable['Movie']:
        return self.__director_movie

    def is_applied_to(self, movie: 'Movie'):
        return movie in self.__director_movie

    def add_movie(self, movie: 'Movie'):
        self.__director_movie.append(movie)

    def __repr__(self):
        return f'<Director {self.__director_full_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.director_full_name == self.director_full_name

    def __lt__(self, other):
        return self.director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()
        self._genre_movie: List[Movie] = list()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    @property
    def genre_movie(self) -> Iterable['Movie']:
        return iter(self._genre_movie)

    @property
    def number_of_genre_movie(self) -> int:
        return len(self._genre_movie)

    def is_applied_to(self, movie: 'Movie'):
        return movie in self._genre_movie

    def add_movie(self, movie: 'Movie'):
        self._genre_movie.append(movie)

    def __repr__(self):
        return f'<Genre {self.__genre_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.genre_name == self.__genre_name

    def __lt__(self, other):
        return self.__genre_name < other.genre_name

    def __hash__(self):
        return hash(self.__genre_name)


class Actor:

    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

        self.__actors_this_one_has_worked_with = set()
        self._actor_movie: List[Movie] = list()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def actor_movie(self) -> Iterable['Movie']:
        return iter(self._actor_movie)

    def add_actor_colleague(self, colleague):
        if isinstance(colleague, self.__class__):
            self.__actors_this_one_has_worked_with.add(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.__actors_this_one_has_worked_with

    def add_movie(self, movie: 'Movie'):
        self._actor_movie.append(movie)

    def is_applied_to(self, movie: 'Movie'):
        return movie in self._actor_movie

    def __repr__(self):
        return f'<Actor {self.__actor_full_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.actor_full_name == self.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)


class User:

    def __init__(self, user_name: str, password: str):
        if user_name == "" or type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name
        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password
        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = 0

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    def watch_movie(self, movie: 'Movie'):
        if isinstance(movie, Movie):
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: 'Review'):
        if isinstance(review, Review):
            self.__reviews.append(review)

    def __repr__(self):
        return f'<User {self.__user_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user_name == self.__user_name

    def __lt__(self, other):
        return self.__user_name < other.user_name

    def __hash__(self):
        return hash(self.__user_name)


class Review:

    def __init__(self, user: User, movie: 'Movie', review_text: str, rating: float, ):
        if isinstance(movie, Movie):
            self.__movie = movie
        else:
            self.__movie = None
        if type(review_text) is str:
            self.__review_text = review_text
        else:
            self.__review_text = None
        if type(rating) is int and 1 <= rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None
        if isinstance(user, User):
            self.__user = user
        else:
            self.__user = None

        self.__timestamp = datetime.now()

    @property
    def movie(self) -> 'Movie':
        return self.__movie

    @property
    def user(self) -> User:
        return self.__user

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.movie == self.__movie and other.review_text == self.__review_text and other.rating == self.__rating and other.timestamp == self.__timestamp

    def __repr__(self):
        return f'<Review of movie {self.__movie}, rating = {self.__rating}, timestamp = {self.__timestamp}>'


class Movie:

    def __set_title_internal(self, title: str):
        if title.strip() == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()

    def __set_release_year_internal(self, release_year: int):
        if int(release_year) >= 1900 and type(release_year) is int:
            self.__release_year = release_year
        else:
            self.__release_year = None

    def __init__(self, title: str, release_year: int):

        self.__set_title_internal(title)
        self.__set_release_year_internal(release_year)

        self.__description = None
        self.__director = []
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None
        self.__review = []
        self.__id = None

    # essential attributes
    @property
    def number_of_review(self) -> int:
        return len(self.__review)

    @property
    def review(self):
        return self.__review

    @property
    def id(self):
        return self.__id

    def set_id(self,id:int):
        self.__id = id

    @property
    def number_of_genres(self) -> int:
        return len(self.__genres)

    @property
    def number_of_actors(self) -> int:
        return len(self.__actors)

    @property
    def number_of_director(self) -> int:
        return len(self.__director)

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__set_title_internal(title)

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        self.__set_release_year_internal(release_year)

    # additional attributes

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if type(description) is str:
            self.__description = description.strip()
        else:
            self.__description = None

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, director: Director):
        if isinstance(director, Director):
            self.__director = director
        else:
            self.__director = None

    def add_director(self, director: Director):
        if not isinstance(director, Director):
            return
        self.__director.append(director)

    @property
    def actors(self) -> list:
        return self.__actors

    def add_actor(self, actor: Actor):
        if not isinstance(actor, Actor) or actor in self.__actors:
            return

        self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if not isinstance(actor, Actor):
            return

        try:
            self.__actors.remove(actor)
        except ValueError:
            # print(f"Movie.remove_actor: Could not find {actor} in list of actors.")
            pass

    @property
    def genres(self) -> list:
        return self.__genres

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre) or genre in self.__genres:
            return

        self.__genres.append(genre)

    def is_genred_by(self, genre: Genre):
        return genre in self.__genres

    def is_genred(self):
        return len(self.__genres) > 0

    def is_directed_by(self, director: Director):
        return director in self.__director

    def is_directed(self):
        return self.__director > 0

    def is_acted_by(self, actor: Actor):
        return actor in self.__actors

    def is_acted(self):
        return len(self.__actors) > 0

    def remove_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return

        try:
            self.__genres.remove(genre)
        except ValueError:
            # print(f"Movie.remove_genre: Could not find {genre} in list of genres.")
            pass

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            return

        self.__review.append(review)

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, val: int):
        if val > 0:
            self.__runtime_minutes = val
        else:
            raise ValueError(f'Movie.runtime_minutes setter: Value out of range {val}')

    def __get_unique_string_rep(self):
        return f"{self.__title}, {self.__release_year}"

    def __repr__(self):
        return f'<Movie {self.__get_unique_string_rep()}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__get_unique_string_rep() == other.__get_unique_string_rep()

    def __lt__(self, other):
        if self.title == other.title:
            return self.release_year < other.release_year
        return self.title < other.title

    def __hash__(self):
        return hash(self.__get_unique_string_rep())


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = []
        self.__dataset_of_actors = set()
        self.__dataset_of_directors = set()
        self.__dataset_of_genres = set()

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            for row in movie_file_reader:
                movie = Movie(row['Title'], int(row['Year']))
                movie.description = row['Description']
                movie.runtime_minutes = int(row['Runtime (Minutes)'])

                director = Director(row['Director'])
                self.__dataset_of_directors.add(director)
                movie.director = director

                parsed_genres = row['Genre'].split(',')
                for genre_string in parsed_genres:
                    genre = Genre(genre_string)
                    self.__dataset_of_genres.add(genre)
                    movie.add_genre(genre)

                parsed_actors = row['Actors'].split(',')
                for actor_string in parsed_actors:
                    actor = Actor(actor_string)
                    self.__dataset_of_actors.add(actor)
                    movie.add_actor(actor)

                self.__dataset_of_movies.append(movie)

    @property
    def dataset_of_movies(self) -> list:
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self) -> set:
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self) -> set:
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres


class ModelException(Exception):
    pass


def make_comment(comment_text: str, user: User, movie: Movie):
    comment = Review(user, movie, comment_text,5)
    user.add_review(comment)
    movie.add_review(comment)

    return comment


def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'genre {genre.genre_name} already applied to movie "{movie.title}"')

    movie.add_genre(genre)
    genre.add_movie(movie)


def make_director_association(movie: Movie, director: Director):
    if director.is_applied_to(movie):
        raise ModelException(f'director{director.director_full_name} already applied to movie "{movie.title}"')

    movie.add_director(director)
    director.add_movie(movie)


def make_actor_association(movie: Movie, actor: Actor):
    if actor.is_applied_to(movie):
        raise ModelException(f'actor {actor.actor_full_name} already applied to movie "{movie.title}"')

    movie.add_actor(actor)
    actor.add_movie(movie)
