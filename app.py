import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Actor, Movie, Gender


def create_app(test_config=None):
    '''
    create and configure the app
    '''
    app = Flask(__name__)
    CORS(app)
    app, db = setup_db(app)
    migrate = Migrate(app, db)

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
