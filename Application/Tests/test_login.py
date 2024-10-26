from flask.testing import FlaskCliRunner, FlaskClient
from flask import session
import pytest
from conftest import *

from Application.Models import User

@pytest.fixture()
def user():
    return User(username="Test12135146549846465471214984864694754", password="myPassIsEASY", email="")

class Test_Login:    
    def test_account_login_fail(self, client:FlaskClient):
        with client:
            response = client.post("/login", data={
                "username": "NO",
                "password": "none"
            })

            assert(len(response.history) == 0)
            assert(response.request.path != "/user") 
            assert("UserId" not in session) #Make sure no cookie is created

    def test_account_creation(self, user:User, client:FlaskClient):
        with client:
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
            assert(session["UserId"] == 1) #testing if cookie is created

    def test_account_login(self, user:User, client:FlaskClient):
        #logout testing
        response = client.get("/logout")
        
        assert(response.json["message"] == "Successful")
        assert(response.json["redirect"] == "/login")
        #-------------

        #We shouldn't be able to access /user
        response = client.get("/user")
        assert(response.status_code == 404)
        #------------------------------------
        
        #try to login
        with client:
            response = client.post("/login", data={
                "username": user.username,
                "password": user.password,
            }, follow_redirects=True)

            #For when the test fails
            print("History:", response.history)
            print("Current Path:", response.request.path)

            assert(response.history[0].status_code == 308)
            assert(response.request.path == "/user") 
            assert(session["UserId"] == 1)

    
    def test_account_recreation(self, user:User, client:FlaskClient):
        #logout
        response = client.get("/logout")
        
        with client:
            response = client.post("/register", data={
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "confirm_password": user.password
            }, follow_redirects=True)

            #For when the test fails
            print("History:", response.history)
            print("Current Path:", response.request.path)

            assert(len(response.history) == 0)
            assert(response.request.path == "/register") 
            assert("UserId" not in session) #testing if cookie is created