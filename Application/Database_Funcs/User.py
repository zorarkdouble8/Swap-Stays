from Application import db
from Application.Models import User

import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#verifies the login and returns a bool
def verify_login(username, password) -> bool:
    try:   
        user = db.session.query(User).filter_by(username = username).first()
    except Exception as e:
        print(e)
        return False

    if (user == None):
        return False
    elif (compare_passwords(password, encrypted_password=user.password)):
        return True
        
#creates a user and return true if it succeeds
def create_user(username, password, email=None) -> bool:
    token = encrypt_password(password)
    new_user = User(username, token, email)

    try:
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as error:
        print(error)
        return False
    
#returns an encrypted password
def encrypt_password(password) -> str:
    type = PBKDF2HMAC(hashes.SHA256(), 32, bytes(os.environ["SALT_KEY"], "utf-8"), 500000)
    key = urlsafe_b64encode(type.derive(bytes(os.environ["ENCRYPT_KEY"], "utf-8")))
    algor = Fernet(key)
    token = algor.encrypt(bytes(password, "utf-8"))

    return token

#compares a password with a encrypted password
#returns true if it's the same
def compare_passwords(password, encrypted_password):
    if (encrypt_password(password) == encrypted_password):
        return True
    else:
        return False