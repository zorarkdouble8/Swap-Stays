from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.template_folder = "./Templates"
app.static_folder = "./Static"

#DATABASE config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../Application/Database.db"
db = SQLAlchemy(app)

#TEMPERORY SECRET KEY
#TODO add github secret key and salt key
os.environ["ENCRYPT_KEY"] = "Temp key!"
os.environ["SALT_KEY"] = "X\x8e\x99\xc8\xa9v\x04oM\xef?F\x86f\xa9\xcd"

#Website INITIALIZATION!
import Application.Models
import Application.Routes