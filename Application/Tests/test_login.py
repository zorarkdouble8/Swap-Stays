import pytest
from conftest import *

@pytest.fixture()
def test1():
    print("TEST111")


def test4(client):
    response = client.get("/")
    print(response)

    assert(3==4)