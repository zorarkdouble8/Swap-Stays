from flask import Flask

app = Flask(__name__)
app.template_folder = "./Templates"


#Website INITIALIZATION!
import Application.Routes