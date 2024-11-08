from Application.Models import Review
from Application import db

def add_review(place_id: int, review_text: str, num_stars: int) -> Review:
    #Add review to database
    #TODO: error handling
    
    new_review = Review(place_id, review_text, num_stars)

    db.session.add(new_review)
    db.session.commit()

    return new_review