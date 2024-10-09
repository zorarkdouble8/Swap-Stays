from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.template_folder = "./Templates"

#DATABASE config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../Application/Database.db"

db = SQLAlchemy(app)

#Website INITIALIZATION!
import Application.Models
import Application.Routes