import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime, date, time
import sys

from dotenv import load_dotenv

load_dotenv()

# my_id = os.getenv('ID')
# key = os.getenv('SECRET_KEY')
# database_name = os.getenv('DATABASE_NAME')
# database_url = os.getenv('DATABASE_URL')
database_path = os.getenv('DATABASE_URL')

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
Base class for common methods
"""
class crudmethods(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
Movie_actor
"""
@dataclass
class Movie_actor(crudmethods):
    __tablename__ = "movie_actor"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    # def insert(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self):
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
            }

"""
Movie

"""
class Movie(crudmethods):
    __tablename__ = 'movies'

    # id = Column(Integer, primary_key=True)
    # title = Column(String)
    # release_date = Column(date)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.Date)
    movie_actor = db.relationship('Movie_actor', backref='movie_parent', lazy=True)
  
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    # def insert(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self):
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
            }

"""
Actor

"""
class Actor(crudmethods):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gend = Column(String)
    movie_actor = db.relationship('Movie_actor', backref='actor_parent', lazy=True)

    def __init__(self, name, age, gend):
        self.name = name
        self.age = age
        self.gend = gend

    # def insert(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self):
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gend': self.gend
            }