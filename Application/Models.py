from Application import app, db

#creates a database if there's no database
with app.app_context():
    db.create_all()

class User(db.Model):
    def __init__(self, username:str, password:str, email:str=None) -> None:
        self.username = username
        self.password = password
        self.email = email

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)

class Place(db.Model):
    #TODO make it to only have specific types and the rating from only 1 to 5
    def __init__(self, name:str, type:str, price:float, amentities:str = None, rating:int = None, campus_distance:float = None) -> None:
        self.place_name = name
        self.place_type = type
        self.price = price
        self.amenities = amentities
        self.rating = rating
        self.campus_distance = campus_distance

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

