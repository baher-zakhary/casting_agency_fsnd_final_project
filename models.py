from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Date, SmallInteger, Enum, String
import enum

username = 'postgres'
password = '0000'
database_name = 'castingAgencyDB'
database_path = "postgres://{}:{}@{}/{}".format(username, password,
                                                "localhost:5432",
                                                database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return (app, db)


'''
actor_movie association table
'''


actor_movie = db.Table('actor_movie',
                       db.Column('actor_id', db.Integer, db.ForeignKey(
                           'actor.id'), primary_key=True),
                       db.Column('movie_id', db.Integer, db.ForeignKey(
                           'movie.id'), primary_key=True)
                       )


'''
Gender Enum
'''


class Gender(enum.Enum):
    male = 0,
    female = 1


'''
Movie
'''


class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    relase_date = Column(Date, nullable=False)

    def __init__(self, title, relase_date):
        self.title = title
        self.relase_date = relase_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'relase_date': self.relase_date
        }

    def format_long(self):
        return {
            'id': self.id,
            'title': self.title,
            'relase_date': self.relase_date,
            'actors': self.actors
        }


'''
Actor
'''


class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(SmallInteger, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    movies = db.relationship('Movie', secondary=actor_movie, lazy='dynamic',
                             backref=db.backref('actors', lazy=True))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def format_long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': self.movies
        }
