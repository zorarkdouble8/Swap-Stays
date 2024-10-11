from flask import render_template
from Application import app
from flask import request
from Application.Login import verify_login

@app.route("/")
def home():
    return render_template("Home/Home.html")

#TODO replace username with the actual user's username?
@app.route("/username")
def userHome():
    return render_template("User/Home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        if (verify_login(request.form["username"], request.form["password"]) == False):
            print("Error, wrong password or username")
        else:
            print("Correct user, login")
        #TODO verify user's credentials
        print(request.form["username"])
        return render_template("Home/Home.html")
    else:
        return render_template("Login/Login.html")
