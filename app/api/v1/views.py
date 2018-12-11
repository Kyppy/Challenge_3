import psycopg2
from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token)
from .models import Database

db = Database()
db.create_tables()


class Interventions(Resource):
    def get(self):
        intervention = db.get_all_interventions()
        return {"status": 200, "data": intervention}, 200
        
    def post(self):
        data = request.get_json(silent=True)
        if data['comment'] is None or data['comment'] is "":
            return{"message": "Incident has missing 'comment' field."}, 400
        if data['type'] == "Redflag" or data['type'] == "Intervention":
            post_data = (data['id'], data['type'], data['location'], 
                         data['Images'], data['Videos'], data['comment'])
            db.insert_intervention(post_data)
            return{"status": 201, "data": [{"id": data['id'], 
                   "message":"Created intervention record"}]}, 201
        return{"message": "Incident is not "
               "type 'Redflag' or 'Intervention'."}, 400


class Intervention(Resource):
    def get(self, intervention_id):
        if intervention_id is None or intervention_id is "":
            return{"message": "No incident id provided"}, 400
        intervention = db.get_intervention(intervention_id)
        if intervention:
            return {"status": 200, "data": intervention}, 200
        return{"message": "No record with id {} exists."
               .format(intervention_id)}, 404

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
        firstname = data["firstname"]
        lastname = data["lastname"]
        if firstname is None or firstname is "":
            return {"message": "Please include your "
                    "firstname and try again."}, 400
        if lastname is None or lastname is "":
            return {"message": "Please include your "
                    "lastname and try again."}, 400
        if username is None or username is "" or password is None or password\
                is ""or email is None or email is "":
            return {"message": "Missing signup parameters.Please check your" 
                    "username,password or email and try again"}, 400
        valid = db.authorise_signup(username, password, email)
        if valid:
            access_token = create_access_token(identity=password)
            post_data = (data['firstname'], data['lastname'], 
                         data['othername'], email, data['phoneNumber'], 
                         username, password, data['isAdmin'])
            db.insert_user(post_data)
            return{"status": 201, "data":
                   [{"token": access_token, "user": data}]}, 201
        return {"message": "Bad credentials.Signup failed"}, 400


class Login(Resource):
    def post(self):
        data = request.get_json(silent=True)
        username = data["username"]
        password = data["password"]
        if username is None or username is "" or\
           password is None or password is "":
            return {"message": "Missing login parameters.Please check your "
                    "username or password and try again."}, 400
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
                 "Updated intervention record comment"}]}, 200


class Interventionstatus(Resource):
    def patch(self, intervention_id):
        data = request.get_json(silent=True)
        admin = data["isAdmin"]
        if admin is False:
            return {"message": "You do not have permission " 
                    "to access this route."}, 403
        incident_type = data['type']
        if incident_type != 'Intervention':
            return {"message": "Invalid incident type. "
                    "Please select an incident of type 'Intervention.'"}, 400
        status = data["status"]
        if status != 'Resolved' or status != 'Rejected':
            return {"message": "Invalid update information"
                    "check your input and try again."}, 400
        patch_data = (status, intervention_id)
        db.update_intervention_status(patch_data)
        return{"status": 200, "data":
               [{"id": intervention_id, "message": 
                 "Updated intervention record status"}]}, 200


class Redflagstatus(Resource):
    def patch(self, red_flag_id):
        data = request.get_json(silent=True)
        admin = data["isAdmin"]
        if admin is False:
            return {"message": "You do not have permission "
                    "to access this route."}, 403
        incident_type = data['type']
        if incident_type != 'Redflag':
            return {"message": "Invalid incident type. "
                    "Please select an incident of type 'Redflag'."}, 400
        status = data["status"]
        if status != 'Resolved' or status != 'Rejected':
            return {"message": "Invalid update information"
                    "check your input and try again."}, 400
        patch_data = (status, red_flag_id)
        db.update_redflag_status(patch_data)
        return{"status": 200, "data":
               [{"id": red_flag_id, "message":
                 "Updated redflag record status"}]}, 200


class Protected(Resource):
    @jwt_required
    def get(self):
        return {"message": "Valid token,access granted"}
 