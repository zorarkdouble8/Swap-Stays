import pytest

@pytest.fixture()
def application():
    from Application import app
    app.testing = True

    return app
    

@pytest.fixture()
def client(application):
    return application.test_client()


@pytest.fixture()
def runner(application):
    return application.test_cli_runner()

