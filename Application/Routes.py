from flask import render_template
from Application import app
from flask import request
from Application.Database_Funcs.User import verify_login, create_user

@app.route("/")
def home():
    return render_template("Home/Home.html")

#TODO replace username with the actual user's username?
@app.route("/username")
def userHome():
    return render_template("User/Home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if (request.method == "POST"):
        if (verify_login(request.form["username"], request.form["password"]) == False):
            error = "Error: wrong password or username"
        else:
            #TODO add cookie to user
            return redirect_logged_in()
    
    return render_template("Login/Login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def createUser():
    error = None
    if (request.method == "POST"):
        #Create a user!
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_pass = request.form["confirm_password"]

        #TODO prevent SQL injection
        if (password == confirm_pass):
            did_create_user = create_user(username, password, email)

            if (did_create_user and verify_login(username, password)):  
                return redirect_logged_in()
            elif (not did_create_user):
                error = "failed to create user, please try again"
            else:
                error = "failed to log user in!"
                #TODO return more descriptive error because usernames are unique
        else:
            error = "Passwords are not equal!"

    return render_template("Login/CreateUser.html", error=error)

#redirects all logged in users to a certain page
#returns: render template
def redirect_logged_in():
    return render_template("Home/Home.html")