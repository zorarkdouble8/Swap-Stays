from Application.Models import Review, Place, User
from Application import db

def add_review(place_id, user: User, review_text, num_stars) -> Review:   
    #TODO: error handling
    
    #Add review to database
    new_review = Review(place_id, user.id, user.username, review_text, num_stars)

    db.session.add(new_review)
    db.session.commit()

    return new_review

def get_reviews_by_place(place_id):
    return Review.query.filter_by(place_id=place_id).all()

def get_reviews_by_user(user_id):
    return Review.query.filter_by(user_id=user_id).all()