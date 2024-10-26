from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskCliRunner, FlaskClient
import pytest

@pytest.fixture(scope="class")
def application() -> Flask:
    from Application import app, db
    app.testing = True
    
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture()
def database() -> SQLAlchemy:
    from Application import db
    return db

@pytest.fixture()
def client(application:Flask) -> FlaskClient:
    client = application.test_client()
    client.allow_subdomain_redirects = True
    return client

@pytest.fixture()
def runner(application:Flask) -> FlaskCliRunner:
    return application.test_cli_runner()

# @pytest.fixture(scope="class")
# def clear_database(application:Flask, database:SQLAlchemy):
#     with application.app_context():
#         database.drop_all()

#     with application.app_context():
#         database.create_all()

