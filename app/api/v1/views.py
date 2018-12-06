import psycopg2
from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token)
from .models import Database

db = Database()
db.create_tables()


class Interventions(Resource):
    def get(self):
        interventions = db.get_all_interventions()
        return {"status": 200, "data": interventions}, 200

    def post(self):
        data = request.get_json(silent=True)
        """
        if data['type'] or data['comment'] is None or "":
            return{"message": "Invalid incident type or comment"}, 400
        """
        post_data = (data['id'], data['type'], data['location'], 
                     data['Images'], data['Videos'], data['comment'])
        db.insert_intervention(post_data)
        return{"status": 200, "data": [{"id": data['id'], 
               "message":"Created intervention record"}]}, 201


class Intervention(Resource):
    def get(self, intervention_id):
        intervention = db.get_intervention(intervention_id)
        return {"status": 200, "data": intervention}, 200
    
    def delete(self, intervention_id):
        db.delete_record(intervention_id)
        return {"status": 200, "data": {"id": intervention_id, 
                "message": "Intervention record has been deleted"}}, 200


class Signup(Resource):
    def post(self):
        data = request.get_json(silent=True)
        username = data["username"]
        password = data["password"]
        email = data["email"]
        if username is None or password is None or email is None:
            return {"message": "Missing signup parameters.Please check your" 
                    "username,password or email and try again"}, 400
        valid = db.authorise_signup(username, password, email)
        if valid:
            access_token = create_access_token(identity=password)
            post_data = (data['firstname'], data['lastname'], 
                         data['othername'], email, data['phoneNumber'], 
                         username, password)
            db.insert_user(post_data)
            return{"status": 201, "data": 
                   [{"token": access_token, "user": data}]}, 201
        return {"message": "Bad credentials.Signup failed"}, 400


class Login(Resource):
    def post(self):
        data = request.get_json(silent=True)
        username = data["username"]
        password = data["password"]
        if username is None or password is None:
            return {"message": "Missing login parameters.Please check your" 
                    "username or password and try again"}, 400
        valid = db.authorise_login(username, password)
        if valid:
            access_token = create_access_token(identity=password)
            return{"status": 200, "data": 
                   [{"token": access_token, "user": data}]}, 200
        return {"message": "Bad credentials.Login failed"}, 400


class Updatelocation(Resource):
    def patch(self, intervention_id):
        data = request.get_json(silent=True)
        location = data["location"]
        if location is None or location is "":
            return {"message": "Missing update information"
                    "check your input and try again"}, 400
        patch_data = (location, intervention_id)
        db.update_intervention_location(patch_data)
        return{"status": 200, "data":
               [{"id": intervention_id, "message": 
                 "Updated intervention record's location"}]}, 200


class Updatecomment(Resource):
    def patch(self, intervention_id):
        data = request.get_json(silent=True)
        comment = data["comment"]
        if comment is None or comment is "":
            return {"message": "Missing update information"
                    "check your input and try again"}, 400
        patch_data = (comment, intervention_id)
        db.update_intervention_comment(patch_data)
        return{"status": 200, "data":
               [{"id": intervention_id, "message": 
                 "Updated intervention record's comment"}]}, 200

 