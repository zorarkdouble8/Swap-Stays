from flask.testing import FlaskCliRunner, FlaskClient
import pytest
from conftest import *

from Application.Models import User

@pytest.fixture()
def user():
    return User(username="Test12135146549846465471214984864694754", password="myPassIsEASY", email="")

class Test_Login:    
    def test_account_creation(self, user:User, client:FlaskClient):
        response = client.post("/register", data={
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "confirm_password": user.password
        }, follow_redirects=True)

        #For when the test fails
        print("History:", response.history)
        print("Current Path:", response.request.path)

        assert(response.history[0].status_code == 308)
        assert(response.request.path == "/user")     
