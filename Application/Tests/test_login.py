import pytest

@pytest.fixture()
def test1():
    print("TEST111")


def test4():
    assert(3==3)