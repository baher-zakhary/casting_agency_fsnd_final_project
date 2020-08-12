from flask_sqlalchemy import SQLAlchemy

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