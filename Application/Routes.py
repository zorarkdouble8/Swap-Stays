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
    if (request.method == "POST"):
        if (verify_login(request.form["username"], request.form["password"]) == False):
            #TODO add error in login page
            print("Error, wrong password or username")
        else:
            #TODO add cookie to user
            return redirect_logged_in()
    else:
        return render_template("Login/Login.html")

@app.route("/register", methods=["GET", "POST"])
def createUser():
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
                print("failed to create user")
            else:
                print("failed to log user in!")
                #TODO return render template with a error
                #TODO return more descriptive error because usernames are unique
        else:
            print("Passwords are not equal!")
            #TODO return template but with message saying passwords arn't equal!

    return render_template("Login/CreateUser.html")

#redirects all logged in users to a certain page
#returns: render template
def redirect_logged_in():
    return render_template("Home/Home.html")