from BaseHandler import BaseHandler

import json
from image_uploader import upload_file
from user_validation import *

class LogoutHandler(BaseHandler):
    def get(self):
        try:
            self.end_session()
            self.write(json.dumps({"success": 1}))
        except:
            self.write(json.dumps({"success": 0}))


class ImageUploadHandler(BaseHandler):
    def post(self):
        try:
            user_profile_image = self.request.files["profile_image"][0]["body"]
            with open("data/tmp.jpeg", "wb+") as file:
                file.write(user_profile_image)
            # Upload to the hosting server retrieving the response and saving this to DB
            secure_url = upload_file()  # TODO: This is hella slow -> MAke Async
            # # Save relevant data to DB
            current_user = self.get_user()
            if not current_user:
                # TODO: This is currently undefined behavior. If no cookie is present when the user logs in, we terminate the operation
                print("NO CURRENT USER?")
                return
            set_user_image(current_user.email_address, secure_url)
            print(secure_url)
            self.write(json.dumps({"success": 1}))
        except Exception as e:
            print(e)
            self.write(json.dumps({"success": 0}))


class LoginHandler(BaseHandler):
    def get(self):
        """
        Login should complete the following operations
        1. Evaluate whether the user exists in the database
        2. If Pass:
            3. Create cryptographic key and add to sessions_db
            4. set_secure_cookie(cryptographic_key)
            4. Redirect user to main page
        5. Else:
            6. Render Error Message on login page ("Invalid Credentials")
        """
        email = self.get_argument("email")
        password = self.get_argument("password")
        if validate_user(email, password):
            # Log User in
            self.set_user(email)
            self.write(json.dumps({"success": 1}))
        else:
            self.write(json.dumps({"success": 0}))


class UserInfoHandler(BaseHandler):
    def get(self):
        print(self.request.body)
        user = self.get_user()
        if user:
            self.write(
                json.dumps(
                    {
                        "success": 1,
                        "username": user.username,
                        "email": user.email_address,
                        "profile_image": user.profile_image,
                        "phone": user.phone,
                    }
                )
            )
        else:
            self.write(json.dumps({"success": 0}))


class UserSignupHandler(BaseHandler):
    def get(self):
        email = self.get_argument("email")
        username = self.get_argument("username")
        password = self.get_argument("password")
        phone = self.get_argument("phone")
        val = register_user(
            username=username, password=password, email=email, phone=phone
        )
        if val:
            self.write(json.dumps({"success": 1}))
        else:
            self.write(json.dumps({"success": 0}))




