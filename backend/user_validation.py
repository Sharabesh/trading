import bcrypt
import secrets
from playhouse.shortcuts import model_to_dict
from functools import reduce
import time
import datetime

from models import *



def register_user(username, email, password, phone) -> bool:
    """
    Adds a user to our database.
    Returns a boolean corresponding to the status code
    of the operation (True for success, False for failure)
    """
    password = password.encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        Users.insert(
            email_address=email, username=username, password=hashed, phone=phone
        ).execute()
    except:
        return False
    return True


def validate_user(email, password):
    """
    Returns True if the user with the provided email
    and password exist in the database. False if either
    user credentials are wrong or another db error occurs
    """
    password = password.encode("utf-8")

    q_handler = (
        Users.select(Users.password).where(Users.email_address == email).execute()
    )

    q_handler = list(q_handler)

    if not q_handler:
        return False

    hashed_pw = q_handler[0].password.encode("utf-8")

    if bcrypt.checkpw(password, hashed_pw):
        return True

    return False


def generate_session_id():
    """
    Generates a cryptographically secure session_id
    to be used as the session_id cookie
    """
    return str(secrets.randbits(32))


def get_user_from_session_id(session_id):
    """
    Returns the user object corresponding to the session_id
    """
    q = Users.select().where(Users.session_id == session_id).execute()

    if q.count == 0:
        return None
    return list(q)[0]


def clear_session_cookie(session_id):
    """
    Deletes the session ID associated with a given user
    For security we unset this on each user login
    """
    Users.update(session_id=None).where(Users.session_id == session_id).execute()


def set_user_token(email, session_id):
    """
    Updates the database with current user token
    """
    Users.update(session_id=session_id).where(Users.email_address == email).execute()


def set_user_image(email, img_url):
    """
    Overwrites the image url associated with an email address
    """
    Users.update(profile_image=img_url).where(Users.email_address == email).execute()
