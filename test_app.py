import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db
import json


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

        self.app, self.db = setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def get_casting_assistant_token(self):
        token = ''
        with open(r'testing_tokens/casting_assistant_token') as reader:
            token = reader.read()
        return token

    def test_get_actors(self):
        token = self.get_casting_assistant_token()
        response = self.client().get(
            '/api/actors',
            headers={"Authorization": token}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['result']))


if __name__ == "__main__":
    unittest.main()
