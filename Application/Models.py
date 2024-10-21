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

from Application import app, db

class Place(db.Model):
    __tablename__ = 'places'

    place_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_name = db.Column(db.String(100), nullable=False)
    place_type = db.Column(db.String(50), nullable=False)  # Updated here
    price = db.Column(db.Numeric(10, 2), nullable=False)
    amenities = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Numeric(3, 2), nullable=True)
    campus_distance = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Place {self.place_name}>'