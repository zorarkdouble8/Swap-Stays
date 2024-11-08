from Application.Models import Review, Place, User
from Application import db

def add_review(place_id, user: User, review_text, num_stars) -> Review:   
    #TODO: error handling
    
    #Add review to database
    new_review = Review(place_id, user.id, user.username, review_text, num_stars)

    db.session.add(new_review)
    db.session.commit()

    return new_review