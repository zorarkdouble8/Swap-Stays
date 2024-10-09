from flask import render_template
from Application import app

@app.route("/")
def home():
    return render_template("Home/Home.html")
