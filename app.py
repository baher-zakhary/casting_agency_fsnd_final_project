import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Actor, Movie, Gender
from auth.auth import requires_auth
from sqlalchemy import and_


def create_app(test_config=None):
    '''
    create and configure the app
    '''
    app = Flask(__name__)
    CORS(app)
    app, db = setup_db(app)
    migrate = Migrate(app, db)

    '''
    Endpoints
    '''

    @app.route('/api/actors', methods=['GET'])
    @requires_auth('read:actor')
    def get_actors(jwt):
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'result': [actor.format() for actor in actors]
        })

    @app.route('/api/movies', methods=['GET'])
    @requires_auth('read:movie')
    def get_movies(jwt):
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'result': [movie.format() for movie in movies]
        })

    @app.route('/api/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).first()
        if actor is None:
            abort(404)
        try:
            actor.delete()
        except Exception:
            abort(500)
        return jsonify({
            'success': True,
            'result': actor_id
        })

    @app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(jwt, movie_id):
        movie = Movie.qurey.filter(Movie.id == movie_id).first()
        if movie is None:
            abort(404)
        try:
            movie.delete()
        except Exception:
            abort(500)
        return jsonify({
            'success': True,
            'result': movie_id
        })

    @app.route('/api/actors', methods=['POST'])
    @requires_auth('add:actor')
    def add_actor(jwt):
        body = request.get_json()
        try:
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            movies = body.get('movies', None)
        except Exception:
            abort(422)
        if name is None or age is None or gender is None:
            abort(400)
        try:
            new_actor = Actor(name=name, age=age, gender=gender)
            if movies is not None:
                new_actor.movies = []
                for movie in movies:
                    title = movie.get('title')
                    release_date = movie.get('release_date')
                    if not title or not release_date:
                        abort(422)
                    movie_found = Movie.query.filter(
                        and_(
                            Movie.title == title,
                            Movie.release_date == release_date
                            )
                    ).first()
                    if movie_found is None:
                        new_movie = Movie(title=title,
                                          release_date=release_date)
                        new_actor.movies.append(new_movie)
                    else:
                        new_actor.movies.append(movie_found)
            new_actor.insert()
        except Exception:
            abort(422)
        return jsonify({
            'success': True,
            'result': [new_actor.format_long()]
        })

    @app.route('/api/movies', methods=['POST'])
    @requires_auth('add:movie')
    def add_movie(jwt):
        body = request.get_json()
        try:
            title = body.get('title', None)
            release_date = body.get('release_date', None)
            actors = json.dumps(body.get('actors', None))
        except Exception:
            abort(422)
        if title is None or release_date is None:
            abort(400)
        try:
            new_movie = Movie(title=title, release_date=release_date,
                              actors=actors)
            new_movie.insert()
        except Exception:
            abort(422)
        return jsonify({
            'success': True,
            'result': [new_movie.format_long()]
        })

    @app.route('/api/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(jwt, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).first()
        if actor is None:
            abort(404)
        try:
            body = request.get_json()
            name = body.get('name', None)
            if name is not None:
                actor.name = name
            age = body.get('age', None)
            if age is not None:
                actor.age = age
            gender = body.get('gender', None)
            if gender is not None:
                actor.gender = gender
            movies = json.dumps(body.get('movies', None))
            if movies is not None:
                actor.movies = movies
            actor.update()
        except Exception:
            abort(422)
        return jsonify({
            'success': True,
            'result': [actor.format_long()]
        })

    @app.route('/api/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie is None:
            abort(404)
        try:
            body = request.get_json()
            title = body.get('title', None)
            if title is not None:
                movie.title = title
            release_date = body.get('release_date', None)
            if release_date is not None:
                movie.release_date = release_date
            actors = body.get('actors', None)
            if actors is not None:
                movie.actors = actors
            movie.update()
        except Exception:
            abort(422)
        return jsonify({
            'success': True,
            'result': [movie.format_long()]
        })

    '''
    Error handlers
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        message = "unprocessable"
        if error.description:
            message = error.description
        return jsonify({
            "success": False,
            "error": 422,
            "message": message
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        message = "resource not found"
        if error.description:
            message = error.description
        return jsonify({
            "success": False,
            "error": 404,
            "message": message
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        message = "Unauthorized"
        if error.description:
            message = error.description
        return jsonify({
            "success": False,
            "error": 401,
            "message": message
        }), 401

    @app.errorhandler(403)
    def unauthorized(error):
        message = "Forbidden"
        if error.description:
            message = error.description
        return jsonify({
            "success": False,
            "error": 403,
            "message": message
        }), 403

    @app.errorhandler(400)
    def bad_request(error):
        message = "Bad request"
        if error.description:
            message = error.description
        return jsonify({
            "success": False,
            "error": 400,
            "message": message
        }), 400

    @app.errorhandler(500)
    def unauthorized(error):
        message = "Internal server error"
        if error.description:
            message = error.description
        return jsonify({
            "success": False,
            "error": 500,
            "message": message
        }), 500

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
