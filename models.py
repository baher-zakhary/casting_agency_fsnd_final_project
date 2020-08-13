from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Date, SmallInteger, Enum, String
import enum

username = 'postgres'
password = 0000
database_name = 'castingAgencyDB'
database_path = "postgres://{}:{}@{}/{}".format(username, password,
                                                "localhost:5432",
                                                database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Gender Enum
'''


class Gender(enum.Enum):
    male = 0,
    female = 1


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
Movie
'''


class Movie():
    id = Column(Integer, primary_key=True)
    relase_date = Column(Date, nullable=False)

    def __init__(self, title, relase_date):
        self.title = title
        self.relase_date = relase_date


'''
Actor
'''


class Actor():
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
