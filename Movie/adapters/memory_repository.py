import csv
import os

from typing import List

from bisect import bisect_left, insort_left

from werkzeug.security import generate_password_hash

from Movie.adapters.repository import AbstractRepository
from Movie.domain.domain_model import Movie, Genre, User, Review, make_genre_association, make_comment,Director,Actor,make_actor_association,make_director_association


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._articles = list()
        self._articles_index = dict()
        self._genres = list()
        self._users = list()
        self._reviews = list()
        self._directors = list()
        self._actors = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username),None)

    def add_movie(self, article: Movie, rank: int, description:str):
        insort_left(self._articles, article)
        article.set_id(rank)
        article.description = description
        self._articles_index[article.id] = article

    def get_movie(self, id: int) -> Movie:
        movie = None

        try:
            movie = self._articles_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_movie_by_year(self, target_date: int) -> List[Movie]:
        matching_articles = list()

        try:
            for movie in self._articles:
                if movie.release_year == target_date:
                    matching_articles.append(movie)
        except ValueError:
            # No articles for specified date. Simply return an empty list.
            pass

        return matching_articles

    def get_number_of_movie(self):
        return len(self._articles)

    def get_first_movie(self):
        article = None

        if len(self._articles) > 0:
            article = self._articles[0]
        return article

    def get_last_movie(self):
        article = None

        if len(self._articles) > 0:
            article = self._articles[-1]
        return article

    def get_movie_by_rank(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self._articles_index]

        # Fetch the Articles.
        articles = [self._articles_index[id] for id in existing_ids]
        return articles

    def get_movie_ranks_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        tag = next((tag for tag in self._genres if tag.genre_name == genre_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if tag is not None:
            article_ids = [article.id for article in tag.genre_movie]
        else:
            # No Tag with name tag_name, so return an empty list.
            article_ids = list()

        return article_ids

    def get_movie_ranks_for_actor(self,actor_name:str):

        actor = next((actor for actor in self._actors if actor.actor_full_name == actor_name),None)

        if actor is not None:
            movie_ids = [movie.id for movie in actor.actor_movie]
        else:
            movie_ids = list()

    def get_movie_ranks_for_director(self, director_name: str):

        director = next((director for director in self._actors if director.director_full_name == director_name), None)

        if director is not None:
            movie_ids = [movie.id for movie in director.actor_movie]
        else:
            movie_ids = list()

    '''
    def get_date_of_previous_article(self, article: Article):
        previous_date = None

        try:
            index = self.article_index(article)
            for stored_article in reversed(self._articles[0:index]):
                if stored_article.date < article.date:
                    previous_date = stored_article.date
                    break
        except ValueError:
            # No earlier articles, so return None.
            pass

        return previous_date

    def get_date_of_next_article(self, article: Article):
        next_date = None

        try:
            index = self.article_index(article)
            for stored_article in self._articles[index + 1:len(self._articles)]:
                if stored_article.date > article.date:
                    next_date = stored_article.date
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_date
    '''

    def add_genre(self, tag: Genre):
        self._genres.append(tag)

    def get_genres(self) -> List[Genre]:
        return self._genres

    def add_director(self,director:Director):
        self._directors.append(director)

    def get_directors(self) -> List[Director]:
        return self._directors

    def add_actor(self,actor:Actor):
        self._actors.append(actor)

    def get_actors(self)->List[Actor]:
        return self._actors

    def add_review(self, comment: Review):
        super().add_review(comment)
        self._reviews.append(comment)

    def get_reviews(self):
        return self._reviews

    # Helper method to return article index.


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_and_genres_and_actors_and_directors(data_path: str, repo: MemoryRepository):
    tags = dict()
    actors = dict()
    directors = dict()

    for data_row in read_csv_file(os.path.join(data_path,'news_articles.csv')):

        article_key = int(data_row[0])
        number_of_tags = len(data_row[2].split())
        article_tags = data_row[2].split(",")
        movie_actors = data_row[5].split(",")
        movie_director = data_row[4]
        movie_description = data_row[3]

        # Add any new tags; associate the current article with tags.
        for tag in article_tags:
            if tag not in tags.keys():
                tags[tag] = list()
            tags[tag].append(article_key)
        #del data_row[-number_of_tags:]

        for actor in movie_actors:
            if actor not in actors.keys():
                actors[actor] = list()
            actors[actor].append(article_key)
        # Create Article object.

        if movie_director not in directors.keys():
            directors[movie_director] = list()
        directors[movie_director].append(article_key)

        movie = Movie(
            title=data_row[1],
            release_year= int(data_row[6])

        )
        repo.add_movie(movie, article_key, movie_description)

    # Create Tag objects, associate them with Articles and add them to the repository.
    for tag_name in tags.keys():
        tag = Genre(tag_name)

        # Add the Article to the repository.

        for article_id in tags[tag_name]:
            movie = repo.get_movie(article_id)
            make_genre_association(movie, tag)
        repo.add_genre(tag)

    for actor_name in actors.keys():
        actor = Actor(actor_name)
        for article_id in actors[actor_name]:
            movie = repo.get_movie(article_id)
            make_actor_association(movie,actor)
        repo.add_actor(actor)

    for director_name in directors.keys():
        director = Director(director_name)
        for movie_id in directors[director_name]:
            movie = repo.get_movie(movie_id)
            make_director_association(movie,director)
        repo.add_director(director)



def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_comments(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
        )
        repo.add_review(comment)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies_and_genres_and_actors_and_directors(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_comments(data_path, repo, users)
