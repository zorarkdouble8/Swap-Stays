from flask import Flask
from flask.testing import FlaskCliRunner, FlaskClient
import pytest

@pytest.fixture()
def application() -> Flask:
    from Application import app
    app.testing = True

    return app
    

@pytest.fixture()
def client(application:Flask) -> FlaskClient:
    client = application.test_client()
    client.allow_subdomain_redirects = True
    return client


@pytest.fixture()
def runner(application:Flask) -> FlaskCliRunner:
    return application.test_cli_runner()

