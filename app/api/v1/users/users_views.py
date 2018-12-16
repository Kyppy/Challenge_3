import psycopg2
import re
from datetime import datetime
from datetime import timedelta
from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token,
                               get_jwt_identity)
from passlib.hash import sha256_crypt
from .setup import Regex
from .users_models import UsersDatabase
reg = Regex()
db = UsersDatabase()
db.create_tables()
expires = timedelta(minutes=60)


class Signup(Resource):
    def post(self):
        data = request.get_json(silent=True)
        superior = False
        password = data["password"]
        username = data["username"]
        email = data["email"]
        first = re.match(reg.names_pattern, data["firstname"])
        last = re.match(reg.names_pattern, data["lastname"])
        other = re.match(reg.othername_pattern, data["othername"])
        mail = re.match(reg.email_pattern, email)
        phone = re.match(reg.phone_pattern, data["phoneNumber"])
        user = re.match(reg.username_pattern, username)
        _pass = re.match(reg.password_pattern, password)
        if first and last and other and mail and phone and user and _pass:
            valid = db.authorise_signup(username, password, email)
            if valid:
                _user = db.user_list()
                if _user is None:
                    superior = True
                hashed = sha256_crypt.hash(password)
                access_token = create_access_token(identity=username,
                                                   expires_delta=expires)
                post_data = (data['firstname'], data['lastname'],
                             data['othername'], email, data['phoneNumber'],
                             username, hashed, superior,)
                db.insert_user(post_data)
                return{"status": 201, "data":
                       [{"token": access_token, "user": "Sign-up Complete!"
                         "Welcome to the app {}!".format(username)}]}, 201
            return {"message": "Bad credentials.Signup failed"}, 400
        return {"message": "Signup failed.Please ensure that your "
                           "credentials are correctly formatted."}, 400


class Login(Resource):
    def post(self):
        data = request.get_json(silent=True)
        username = data["username"]
        password = data["password"]
        invalid_user = ("", None)
        invalid_password = ("", None)
        if username in invalid_user or password in invalid_password:
            return {"message": "Missing login parameters.Please check your "
                    "username or password and try again."}, 400
        valid = db.check_valid(username, password)
        if valid:
            access_token = create_access_token(identity=username,
                                               expires_delta=expires)
            return{"status": 200, "data":
                   [{"token": access_token, "user": "Login successful."
                     "Welcome back {}!".format(username)}]}, 200
        return {"message": "Bad credentials.Login failed"}, 400