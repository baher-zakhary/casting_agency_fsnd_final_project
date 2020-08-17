import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
import json
import enum


class RoleTokenEnum(enum.Enum):
    casting_assistant_token = 0,
    casting_director_token = 1,
    executive_producer_token = 2


class CastingAgencyTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.username = "postgres"
        self.password = "0000"
        self.database_name = "casting_agency_testing_DB"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            self.username,
            self.password,
            "localhost:5432",
            self.database_name
        )

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def get_token(self, roleToken):
        token = ''
        with open(r'testing_tokens/' + roleToken) as reader:
            token = reader.read()
        return token

    def test_get_actors_success(self):
        token = self.get_token(RoleTokenEnum.casting_assistant_token.name)
        response = self.client().get(
            '/api/actors',
            headers={"Authorization": token}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['result']))

    def test_get_movies_success(self):
        token = self.get_token(RoleTokenEnum.casting_assistant_token.name)
        response = self.client().get(
            '/api/movies',
            headers={'Authorization': token}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['result']))

    def test_add_actor_success(self):
        token = self.get_token(RoleTokenEnum.casting_director_token.name)
        new_actor = {
            "name": "test actor",
            "age": 23,
            "gender": "male"
        }
        response = self.client().post(
            '/api/actors',
            headers={"Authorization": token},
            json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.inserted_actor = Actor.query.filter(
            Actor.id == data['result'][0]['id']
        ).first()
        self.assertEqual(self.inserted_actor.name, "test actor")
        self.assertEqual(self.inserted_actor.age, 23)
        self.assertEqual(self.inserted_actor.gender.name, "male")

    def test_update_actor_success(self):
        token = self.get_token(RoleTokenEnum.casting_director_token.name)
        actor_to_update = Actor.query.first()
        actor_update = {
            "name": "Actor updated test",
            "age": 50,
            "gender": "female"
        }
        response = self.client().patch(
            '/api/actors/' + str(actor_to_update.id),
            headers={"Authorization": token},
            json=actor_update
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.updated_actor = Actor.query.filter(
            Actor.id == data['result'][0]['id']
        ).first()
        self.assertEqual(
            self.updated_actor.name,
            "Actor updated test"
        )
        self.assertEqual(self.updated_actor.age, 50)
        self.assertEqual(self.updated_actor.gender.name, "female")

    def test_delete_actor_success(self):
        token = self.get_token(RoleTokenEnum.casting_director_token.name)
        actor_to_delete = Actor.query.first()
        response = self.client().delete(
            '/api/actors/' + str(actor_to_delete.id),
            headers={"Authorization": token}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.deleted_actor = Actor.query.filter(
            Actor.id == data['result']
        ).first()
        self.assertEqual(self.deleted_actor, None)

    def test_add_movie_success(self):
        token = self.get_token(RoleTokenEnum.executive_producer_token.name)
        new_movie = {
            "title": "movie new",
            "release_date": "2020-08-16",
        }
        response = self.client().post(
            '/api/movies',
            headers={"Authorization": token},
            json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.inserted_movie = Movie.query.filter(
            Movie.id == data['result'][0]['id']
        ).first()
        self.assertEqual(self.inserted_movie.title, "movie new")
        self.assertEqual(str(self.inserted_movie.release_date), "2020-08-16")

    def test_update_movie_success(self):
        token = self.get_token(RoleTokenEnum.executive_producer_token.name)
        movie_to_update = Movie.query.first()
        movie_update = {
            "title": "movie updated",
            "release_date": "2020-08-16",
        }
        response = self.client().patch(
            '/api/movies/' + str(movie_to_update.id),
            headers={"Authorization": token},
            json=movie_update
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.updated_movie = Movie.query.filter(
            Movie.id == data['result'][0]['id']
        ).first()
        self.assertEqual(
            self.updated_movie.title,
            "movie updated"
        )
        self.assertEqual(str(self.updated_movie.release_date), "2020-08-16")

    def test_delete_movie_success(self):
        token = self.get_token(RoleTokenEnum.executive_producer_token.name)
        movie_to_delete = Movie.query.first()
        response = self.client().delete(
            '/api/movies/' + str(movie_to_delete.id),
            headers={"Authorization": token}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.deleted_movie = Movie.query.filter(
            Movie.id == data['result']
        ).first()
        self.assertEqual(self.deleted_movie, None)

    def test_get_actors_error(self):
        response = self.client().get(
            '/api/actors'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_movies_error(self):
        response = self.client().get(
            '/api/movies',
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_actor_error(self):
        token = self.get_token(RoleTokenEnum.casting_director_token.name)
        new_actor = {
            "nam": "test actor",
        }
        response = self.client().post(
            '/api/actors',
            headers={"Authorization": token},
            json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_update_actor_error(self):
        token = self.get_token(RoleTokenEnum.casting_director_token.name)
        actor_to_update = Actor.query.first()
        response = self.client().patch(
            '/api/actors/' + str(actor_to_update.id),
            headers={"Authorization": token},
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

    def test_delete_actor_error(self):
        token = self.get_token(RoleTokenEnum.casting_director_token.name)
        response = self.client().delete(
            '/api/actors/-1',
            headers={"Authorization": token}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_add_movie_error(self):
        token = self.get_token(RoleTokenEnum.executive_producer_token.name)
        new_movie = {
            "titl": "movie new"
        }
        response = self.client().post(
            '/api/movies',
            headers={"Authorization": token},
            json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

    def test_update_movie_error(self):
        token = self.get_token(RoleTokenEnum.executive_producer_token.name)
        movie_to_update = Movie.query.first()
        response = self.client().patch(
            '/api/movies/' + str(movie_to_update.id),
            headers={"Authorization": token}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

    def test_delete_movie_error(self):
        token = self.get_token(RoleTokenEnum.executive_producer_token.name)
        response = self.client().delete(
            '/api/movies/-1',
            headers={"Authorization": token}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    unittest.main()
