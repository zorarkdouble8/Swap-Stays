from flask import render_template, redirect
from Application import app
from flask import request, session
from Application.Database_Funcs.User import *
from Application.Models import User

@app.route("/")
def home():
    return render_template("Home/Home.html")

#TODO replace username with the actual user's username?
@app.route("/user")
def userHome():
    if ("UserId" in session):
        user_id = session["UserId"]

        user = get_user(user_id)

        return render_template("User/Home.html", user=user)
    else:
        print("Not logged in!")

        return render_template("Error/404.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if (is_logged_in()):
        return redirect("/user")

    if (request.method == "POST"):
        user = verify_login(request.form["username"], request.form["password"])
        if (user == None):
            error = "Error: wrong password or username"
        else:
            return redirect_logged_in(user)
    
    return render_template("Login/Login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def createUser():
    error = None

    if (is_logged_in()):
        return redirect("/user")

    if (request.method == "POST"):
        #Create a user!
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_pass = request.form["confirm_password"]

        #TODO prevent SQL injection
        if (password == confirm_pass):
            user = create_user(username, password, email)

            if (user != None and verify_login(username, password)):  
                return redirect_logged_in(user)
            elif (user != None):
                error = "failed to create user, please try again" #TODO Perhaps because usernames are unique
            else:
                error = "failed to log user in!" #TODO Perhaps because usernames are unique
        else:
            error = "Passwords are not equal!"

    return render_template("Login/CreateUser.html", error=error)

#redirects all logged in users to a certain page
#returns: render template
def redirect_logged_in(user: User):
    print("User: ", user)
    #create cookie
    session["UserId"] = user.id

    return redirect("/user")

#checks the cookie to determine if there's a user logged in
def is_logged_in() -> bool:
    if ("UserId" in session):
        return True
    else:
        return False
