from Application.Models import List
from Application import db

def add_list(list:List)->None:
    #TODO: add error handling

    db.session.add(list)
    db.session.commit()

def remove_list(list:List)->None:
    #TODO: add error handling

    db.session.delete(list)
    db.session.commit()