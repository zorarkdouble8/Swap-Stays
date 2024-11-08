from Application.Models import Review
from Application import db

def add_review(place_id: int, review_text: str, num_stars: int) -> Review:   
    #TODO: error handling
    
    #Add review to database
    new_review = Review(place_id, review_text, num_stars)

    db.session.add(new_review)
    db.session.commit()

    return new_review

# def return_reviews(place_id:int) -> Review:
#     #TODO: add error handling

#     #get reviews from foreign key
#     reviews = db.session.get()