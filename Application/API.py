from Application import app
from flask import session
from Application.Database_Funcs.User import *

#logs the user out and clears the cookies
@app.route("/logout")
def logout():
    session.clear()

    return { "message": "Successful", "redirect": "/login" }
