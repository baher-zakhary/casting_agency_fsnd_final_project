## Casting Agency FSND Final Project

  

### Motivation
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Local development instructions
- Create and activate virtual environment
- Install requirements
	```bash
	pip install -r requirements.txt
	```
- Create Database
	```bash
	psql createdb casting_agency_DB
	# if not working, try
	psql -U <username>
	enter your user password
	# in psql shell
	create database "<database_name>";
	# quit psql shell
	\q
	```
- In models.py fill in database connection attributes

- Restore tables & mock data
	```bash
	psql -U <username> casting_agency_DB < casting_agency_db.psql
	```
- Run app
	```
	python app.py
	```
### Running unit tests

- Create and activate virtual environment
- Install requirements
	```bash
	pip install -r requirements.txt
	```
- Create Database for testing
	```bash
	psql dropdb casting_agency_testing_DB
	psql createdb casting_agency_testing_DB
	# if not working, try
	psql -U <username>
	enter your user password
	# in psql shell
	create database "<database_name>";
	# quit psql shell
	\q
	```
- Restore tables & mock data
	```bash
	psql -U <username> casting_agency_testing_DB < casting_agency_db.psql
	```
- Run unit tests
	```
	python test_app.py
	```
**Note:** In `/testing_tokens` you will find files that contain tokens used by tests, tokens where set to expire after maximum possible period allowed by Auth0 which is 24hrs, if they expired you need to go to `/auth/test_users_credentials.txt`
where you will find the login link and the credentials to three users of our three roles.
You need to login with each user and renew the tokens stored in 	`/testing_tokens` for the test to run successfully
	

### API Documentation:

- **GET** /api/actors
	- **Description:** Fetches a list of all actors
	- **Request Arguments:** None
	- **Returns:** An object with keys
		- **result,** that contains a list of actors
		- **success,** that contains a boolean to indicate success or failure status

- **GET** /api/movies
	- **Description:** Fetches a list of all movies
	- **Request Arguments:** None
	- **Returns:** An object with keys
		- **result,** that contains a list of movies
		- **success,** that contains a boolean to indicate success or failure status

- **DELETE** /api/actors/&lt;int:id&gt;

	- **Description:** Deletes an actor with the provided ID
	- **Request Arguments:**
		- **id:** route parameter of the id of the actor to be deleted
	- **Returns:** An object with keys
		- **result,** contains the id of the deleted actor
		- **success,** that contains a boolean to indicate success or failure status

- **DELETE** /api/movies/&lt;int:id&gt;

	- **Description:** Deletes a movie with the provided ID
	- **Request Arguments:**
		- **id:** route parameter of the id of the movie to be deleted
	- **Returns:** An object with keys
		- **result,** contains the id of the deleted actor
		- **success,** that contains a boolean to indicate success or failure status

- **POST** /api/actors

	- **Description:** Adds a new actor
	- **Request Arguments:**
		- The actor as a JSON object in the request body
	- **Returns:** An object with keys
		- **result,** a list containing the added actor
		- **success,** that contains a boolean to indicate success or failure status

- **POST** /api/movies

	- **Description:** Adds a new movie
	- **Request Arguments:**
		- The movie as a JSON object in the request body
	- **Returns:** An object with keys
		- **result,** a list containing the added movie
		- **success,** that contains a boolean to indicate success or failure status

- **PATCH** /api/actors/&lt;int:id&gt;

	- **Description:** Updates an actor
	- **Request arguments:**
		- The actor ID to update as a route parameter
		- New actor properties as a JSON object in the request body
	- **Returns:** An object with keys
		- **result,** a list containing the updated actor
		- **success,** that contains a boolean to indicate success or failure 


- **PATCH** /api/movies/&lt;int:id&gt;

	- **Description:** Updates a movie
	- **Request arguments:**
		- The movie ID to update as a route parameter
		- New actor properties as a JSON object in the request body
	- **Returns:** An object with keys
		- **result,** a list containing the updated movie
		- **success,** that contains a boolean to indicate success or failure 

### Roles:

- Casting Assistant
	- **Permissions:**
		- Can view actors and movies

- Casting Director
	- **Permissions:**
		- All permissions a Casting Assistant has and…
		- Add or delete an actor from the database
		- Modify actors or movies

- Executive Producer
	- **Permissions:**
		- All permissions a Casting Director has and…
		- Add or delete a movie from the database

### Tests:

- One test for success behavior of each endpoint

- One test for error behavior of each endpoint

- At least two tests of RBAC for each role