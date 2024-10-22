from Application import app, db
from datetime import date

# Creates the database if it doesn't exist
with app.app_context():
    db.create_all()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)

    def __init__(self, username: str, password: str, email: str = None) -> None:
        self.username = username
        self.password = password
        self.email = email

class Place(db.Model):
    __tablename__ = 'places'

    place_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_name = db.Column(db.String(100), nullable=False)
    place_type = db.Column(db.String(50), nullable=False)  # Either 'Hotel' or 'Airbnb'
    price = db.Column(db.Numeric(10, 2), nullable=False)
    amenities = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Numeric(3, 2), nullable=True)  # Rating from 1.0 to 5.0
    campus_distance = db.Column(db.String(20), nullable=True)  # Distance from campus in miles
    guests_num = db.Column(db.Integer, nullable=False)  # Number of guests
    available_from = db.Column(db.Date, nullable=False)  # Available start date
    available_to = db.Column(db.Date, nullable=False)  # Available end date

    def __init__(
        self, place_name: str, place_type: str, price: float, amenities: str = None,
        rating: float = None, campus_distance: str = None, guests_num: int = None,
        available_from: date = None, available_to: date = None
    ) -> None:
        self.place_name = place_name
        self.place_type = place_type
        self.price = price
        self.amenities = amenities
        self.rating = rating
        self.campus_distance = campus_distance
        self.guests_num = guests_num
        self.available_from = available_from
        self.available_to = available_to

    def __repr__(self):
        return f'<Place {self.place_name}>'

# Ensuring all models are created in the database
with app.app_context():
    db.create_all()
