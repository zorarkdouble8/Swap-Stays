from Application.Models import Review, Place, User
from Application import db

def add_review(place_id, user_id, username, review_text, num_stars) -> Review:
    try:
        # Create a new review instance
        new_review = Review(place_id, user_id, username, review_text, num_stars)
        
        # Add to the database session and commit
        db.session.add(new_review)
        db.session.commit()

        return new_review
    except Exception as e:
        print(f"Error adding review: {e}")
        db.session.rollback()
        return None

def get_reviews_by_place(place_id):
    # Return all reviews for a specific place
    return Review.query.filter_by(place_id=place_id).all()

def get_reviews_by_user(user_id):
    # Return all reviews by a specific user
    return Review.query.filter_by(user_id=user_id).all()
