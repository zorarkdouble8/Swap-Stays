from Application.Models import Place
from Application import db

# Function to retrieve all places from the database
#TODO add error handling
def get_places() -> Place:
    return Place.query.all()

# Function to add a new place to the database
def add_place(place_name, place_type, price, amenities, rating, campus_distance) -> Place:
    try:
        new_place = Place(
            place_name=place_name,
            type=place_type,
            price=price,
            amenities=amenities,
            rating=rating,
            campus_distance=campus_distance
        )
        db.session.add(new_place)
        db.session.commit()
        return new_place
    except Exception as e:
        print(f"Error adding place: {e}")
        db.session.rollback()
        return None
