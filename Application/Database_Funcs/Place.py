from Application.Models import Place
from Application import db
from datetime import date

# Function to retrieve all places from the database
# TODO: add error handling
def get_places() -> Place:
    return Place.query.all()

# TODO: add error handling
def get_place(place_id: int) -> Place:
    return db.session.get_one(Place, place_id)

# Function to add a new place to the database
def add_place(
    place_name: str, place_type: str, price: float, amenities: str, 
    rating: float, campus_distance: str, guests_num: int, 
    available_from: date, available_to: date
) -> Place:
    try:
        new_place = Place(
            place_name=place_name,
            place_type=place_type,  # Use `place_type` correctly here
            price=price,
            amenities=amenities,
            rating=rating,
            campus_distance=campus_distance,
            guests_num=guests_num,
            available_from=available_from,  # Add date range
            available_to=available_to       # Add date range
        )
        db.session.add(new_place)
        db.session.commit()
        return new_place
    except Exception as e:
        print(f"Error adding place: {e}")
        db.session.rollback()
        return None

# Function to add a new place to the database
def add_place(
    place_name: str, place_type: str, price: float, amenities: str, 
    rating: float, campus_distance: str, guests_num: int, 
    available_from: date, available_to: date
) -> Place:
    try:
        new_place = Place(
            place_name=place_name,
            place_type=place_type,
            price=price,
            amenities=amenities,
            rating=rating,
            campus_distance=campus_distance,
            guests_num=guests_num,
            available_from=available_from,
            available_to=available_to
        )
        db.session.add(new_place)
        db.session.commit()
        return new_place
    except Exception as e:
        print(f"Error adding place: {e}")
        db.session.rollback()
        return None

# Function to search for places based on criteria
from datetime import datetime, timedelta

def search_places(guests: int = None, checkin: str = None, checkout: str = None, campus_distance: str = None) -> list:
    try:
        # Start with the base query
        query = Place.query

        # Filter by number of guests
        if guests is not None:
            query = query.filter(Place.guests_num >= guests)

        # Handle check-in and check-out dates
        if checkin:
            available_from = datetime.strptime(checkin, '%Y-%m-%d').date()
            query = query.filter(Place.available_from <= available_from)
        if checkout:
            available_to = datetime.strptime(checkout, '%Y-%m-%d').date()
            query = query.filter(Place.available_to >= available_to)

        # Filter by campus distance
        if campus_distance:
            query = query.filter(Place.campus_distance == campus_distance)

        # Return filtered results
        return query.all()
    except Exception as e:
        print(f"Error searching for places: {e}")
        return []
