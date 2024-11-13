from Application import db, app
from datetime import date

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)

    # Define one relationship to reviews
    reviews = db.relationship('Review', back_populates='user', lazy=True)

    def __init__(self, username, password, email=None):
        self.username = username
        self.password = password
        self.email = email

# Place Model
class Place(db.Model):
    __tablename__ = 'places'
    place_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    place_name = db.Column(db.String(100), nullable=False)
    place_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    amenities = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Numeric(3, 2), nullable=True)
    campus_distance = db.Column(db.String(20), nullable=True)
    guests_num = db.Column(db.Integer, nullable=False)
    available_from = db.Column(db.Date, nullable=False)
    available_to = db.Column(db.Date, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)  # Path to image
    address = db.Column(db.String(255), nullable=True)

    # Relationship to reviews
    reviews = db.relationship('Review', back_populates='place', lazy='dynamic')

    def __init__(self, place_name, place_type, price, amenities, rating, campus_distance, guests_num, available_from, available_to, image_path=None, address=None):
        self.place_name = place_name
        self.place_type = place_type
        self.price = price
        self.amenities = amenities
        self.rating = rating
        self.campus_distance = campus_distance
        self.guests_num = guests_num
        self.available_from = available_from
        self.available_to = available_to
        self.image_path = image_path
        self.address = address  # Initialize the address attribute

# Review Model
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.place_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    review = db.Column(db.Text, nullable=False)
    stars = db.Column(db.Numeric(3, 2), nullable=False)

    # Backpopulates for relationships
    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    def __init__(self, place_id, user_id, username, review, stars):
        self.place_id = place_id
        self.user_id = user_id
        self.username = username
        self.review = review
        self.stars = stars

# Create tables in the database
with app.app_context():
    db.create_all()
    print("Database tables created.")
