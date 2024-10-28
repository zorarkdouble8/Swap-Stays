from flask import Flask, render_template
from Application import app

@app.errorhandler(404)
def page_not_found(error):
    return render_template("Error/404.html"), 404
