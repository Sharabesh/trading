import tornado.web
import tornado.websocket

from image_uploader import upload_file
from user_validation import *


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")

    def set_user(self, email):
        user_token = generate_session_id()
        set_user_token(email, user_token)
        self.set_secure_cookie("SESSION_ID", user_token, httponly=True)

    def get_user(self):
        session_id = self.get_secure_cookie("SESSION_ID")
        if not session_id:
            return None
        session_id = session_id.decode("utf-8")
        user = get_user_from_session_id(session_id)
        return user

    def end_session(self):
        session_id = self.get_secure_cookie("SESSION_ID")
        if not session_id:
            return
        session_id = session_id.decode("utf-8")
        clear_session_cookie(session_id)
        self.clear_cookie("SESSION_ID")