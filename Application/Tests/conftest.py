from Application import app
import pytest

@pytest.fixture()
def test():
    assert(3==3)

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

