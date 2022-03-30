# Todolist API
A basic API that allows users to create to-do tasks.
This project uses Django REST Framework with JWT authentication for users.

## Install
Clone the repository using:
```bash
$ git clone https://github.com/Shizuku-Asami/todolist
```
Create a virtual environment inside the project's directory:
```bash
$ python -m venv venv
```
Activate the virtual environment:
```bash
$ source venv/bin/activate
```
Create a `.env` file inside the project's root and add the following configurations:
```.env
DEBUG=True
SECRET_KEY=yoursecretkey
DATABASE_URL=psql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}
STATIC_URL=/static/
```
If you prefer SQLite over PostgreSQL then you can use this instead:
```.env
DATABASE_URL=sqlite://todolist.sqlite3
```
Run the command
```bash
(venv) $ poetry install
```
to install the dependencies.

Make sure that you create a database for the project and then run the command
```bash
(venv) $ python manage.py migrate
```
to create database tables.

If you want to run the server in development mode use the command:
```bash
(venv) $ python manage.py runserver --settings=todolist.settings.development
```
Or you can run the server in production mode using:
```bash
(venv) $ python manage.py runserver --settings=todolist.settings.production
```
## Install using Docker image
Coming soon.

## Running tests
This project uses pytest for testing. To run all the tests:
```bash
(venv) $ pytest -v
```
If all the tests pass then you're good to go.