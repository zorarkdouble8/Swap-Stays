from Application import app, db

class User(db.Model):
    def __init__(self, username, password, email=None):
        self.username = username
        self.password = password
        self.email = email

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)

#creates a database if there's no database
with app.app_context():
    db.create_all()