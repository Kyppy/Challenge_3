import psycopg2
import datetime
import re
from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token)
from .models import Database


db = Database()
db.create_tables()
now = datetime.datetime.now()
id_pattern = re.compile(r'^[0-9]+$')


class Interventions(Resource):
    def get(self):
        intervention_list = []
        inter = db.get_all_interventions()
        for inter in inter:
            inter_data = {"id": inter[0], "createdOn": inter[1],
                          "createdBy": inter[2], "type": inter[3],
                          "location": inter[4], "status": inter[5],
                          "Images": inter[6], "Videos": inter[7],
                          "comment": inter[8]}
            intervention_list.append(inter_data)
        return {"status": 200, "data": intervention_list}, 200

    def post(self):
        data = request.get_json(silent=True)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        if data['comment'] is None or data['comment'] is "":
            return{"message": "Intervention has missing 'comment' field."}, 400
        if data['type'] == "Intervention":
            post_data = (data['type'], data['location'],
                         data['Images'], data['Videos'],
                         data['comment'], timestamp)
            db.insert_intervention(post_data)
            _id = db.get_latest_id()
            return{"status": 201, "data": [{"id": _id[0], 
                   "message": "Created intervention record"}]}, 201
        return{"message": "Incident is not "
               "type 'Intervention'."}, 400


class Redflags(Resource):
    def get(self):
        redflag_list = []
        red = db.get_all_redflags()
        for red in red:
            red_data = {"id": red[0], "createdOn": red[1],
                        "createdBy": red[2], "type": red[3],
                        "location": red[4], "status": red[5],
                        "Images": red[6], "Videos": red[7],
                        "comment": red[8]}
            redflag_list.append(red_data)
        return {"status": 200, "data": redflag_list}, 200

    def post(self):
        data = request.get_json(silent=True)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        if data['comment'] is None or data['comment'] is "":
            return{"message": "Redflag has missing 'comment' field."}, 400
        if data['type'] == "Redflag":
            post_data = (data['type'], data['location'],
                         data['Images'], data['Videos'],
                         data['comment'], timestamp)
            db.insert_intervention(post_data)
            _id = db.get_latest_id()
            return{"status": 201, "data": [{"id": _id[0],
                   "message": "Created redflag record"}]}, 201
        return{"message": "Incident is not "
               "type 'Redflag'."}, 400


class Intervention(Resource):
    def get(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
            intervention_list = []
            if intervention_id is None or intervention_id is "":
                return{"message": "No incident id provided"}, 400
            inter = db.get_intervention(intervention_id)
            if inter:
                inter_data = {"id": intervention_id, "createdOn": inter[1],
                              "createdBy": inter[2], "type": inter[3],
                              "location": inter[4], "status": inter[5],
                              "Images": inter[6], "Videos": inter[7],
                              "comment": inter[8]}
                intervention_list.append(inter_data)
                return {"status": 200, "data": intervention_list}, 200
            return{"message": "No intervention record with id {} exists."
                   .format(intervention_id)}, 404
        return {"message": "Invalid incident id in URL"}

    def delete(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
            if intervention_id is None or intervention_id is "":
                return{"message": "No incident id provided"}, 400
            inter = db.get_intervention(intervention_id)
            if inter:
                db.delete_record(intervention_id)
                return {"status": 200, "data": [{"id": intervention_id,
                        "message": "Intervention record "
                                                 "has been deleted"}]}, 200
            return{"message": "No intervention record with id {} exists."
                   .format(intervention_id)}, 404
        return {"message": "Invalid incident id in URL"}


class Redflag(Resource):
    def get(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
            redflag_list = []
            if redflag_id is None or redflag_id is "":
                return{"message": "No incident id provided"}, 400
            red = db.get_redflag(redflag_id)
            if red:
                red_data = {"id": redflag_id, "createdOn": red[1],
                            "createdBy": red[2], "type": red[3],
                            "location": red[4], "status": red[5],
                            "Images": red[6], "Videos": red[7],
                            "comment": red[8]}
                redflag_list.append(red_data)
                return {"status": 200, "data": redflag_list}, 200
            return{"message": "No redflag record with id {} exists."
                   .format(redflag_id)}, 404
        return {"message": "Invalid incident id in URL"}

    def delete(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
            if redflag_id is None or redflag_id is "":
                return{"message": "No incident id provided"}, 400
            red = db.get_redflag(redflag_id)
            if red:
                db.delete_record(redflag_id)
                return {"status": 200, "data": [{"id": redflag_id,
                        "message": "Redflag record has been deleted"}]}, 200
            return{"message": "No redflag record with id {} exists."
                   .format(redflag_id)}, 404
        return {"message": "Invalid incident id in URL"}


class Signup(Resource):
    def post(self):
        data = request.get_json(silent=True)
        firstname = data["firstname"]
        lastname = data["lastname"]
        othername = data["othername"]
        email = data["email"]
        phone_num = data["phoneNumber"]
        username = data["username"]
        password = data["password"]
        names_pattern = re.compile(r'^[a-zA-Z]{1,25}$')
        othername_pattern = re.compile(r'^[a-zA-Z]{0,25}$')
        email_pattern = re.compile(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+$')
        phone_pattern = re.compile(r'\d{3}-\d{3}-\d{4}')
        username_pattern = re.compile(r'^[a-zA-z0-9_.+!?@&-]{1,25}$')
        password_pattern = re.compile(r'^[a-zA-z0-9_.+!?@&-]{1,50}$')
        first = re.match(names_pattern, firstname)
        last = re.match(names_pattern, lastname)
        other = re.match(othername_pattern, othername)
        mail = re.match(email_pattern, email)
        phone = re.match(phone_pattern, phone_num)
        user = re.match(username_pattern, username)
        _pass = re.match(password_pattern, password)
        if first and last and other and mail and phone and user and _pass:
            valid = db.authorise_signup(username, password, email)
            if valid:
                access_token = create_access_token(identity=username)
                post_data = (data['firstname'], data['lastname'],
                             data['othername'], email, data['phoneNumber'],
                             username, password, data['isAdmin'])
                db.insert_user(post_data)
                return{"status": 201, "data":
                       [{"token": access_token, "user": data}]}, 201
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
        valid = db.authorise_login(username, password)
        if valid:
            access_token = create_access_token(identity=username)
            return{"status": 200, "data":
                   [{"token": access_token, "user": data}]}, 200
        return {"message": "Bad credentials.Login failed"}, 400


class UpdateInterventionLocation(Resource):
    def patch(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            location = data["location"]
            if location is None or location is "":
                return {"message": "Missing update information"
                        "check your input and try again"}, 400
            inter = db.get_intervention(intervention_id)
            if inter:
                patch_data = (location, intervention_id)
                db.update_intervention_location(patch_data)
                return{"status": 200, "data":
                       [{"id": intervention_id, "message": 
                        "Updated intervention record's location"}]}, 200
            return{"message": "No record with id {} exists."
                   .format(intervention_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400


class UpdateRedflagLocation(Resource):
    def patch(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            location = data["location"]
            if location is None or location is "":
                return {"message": "Missing update information"
                        "check your input and try again"}, 400
            inter = db.get_redflag(redflag_id)
            if inter:
                patch_data = (location, redflag_id)
                db.update_intervention_location(patch_data)
                return{"status": 200, "data":
                       [{"id": redflag_id, "message":
                        "Updated redflag record's location"}]}, 200
            return{"message": "No record with id {} exists."
                   .format(redflag_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400


class UpdateInterventionComment(Resource):
    def patch(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            comment = data["comment"]
            if comment is None or comment is "":
                return {"message": "Missing update information"
                        "check your input and try again"}, 400
            inter = db.get_intervention(intervention_id)
            if inter:
                patch_data = (comment, intervention_id)
                db.update_intervention_comment(patch_data)
                return{"status": 200, "data":
                       [{"id": intervention_id, "message": 
                        "Updated intervention record comment"}]}, 200
            return{"message": "No record with id {} exists."
                   .format(intervention_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400


class UpdateRedflagComment(Resource):
    def patch(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            comment = data["comment"]
            if comment is None or comment is "":
                return {"message": "Missing update information"
                        "check your input and try again"}, 400
            inter = db.get_redflag(redflag_id)
            if inter:
                patch_data = (comment, redflag_id)
                db.update_intervention_comment(patch_data)
                return{"status": 200, "data":
                       [{"id": redflag_id, "message":
                        "Updated redflag record comment"}]}, 200
            return{"message": "No record with id {} exists."
                   .format(redflag_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400


class Interventionstatus(Resource):
    def patch(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            admin = data["isAdmin"]
            if admin is False:
                return {"message": "You do not have permission " 
                        "to access this route."}, 403
            incident_type = data['type']
            if incident_type != 'Intervention':
                return {"message": "Invalid incident type. "
                        "Please select an incident "
                        "of type 'Intervention.'"}, 400
            status = data["status"]
            if status != 'Resolved' or status != 'Rejected':
                return {"message": "Invalid update information"
                        "check your input and try again."}, 400
            inter = db.get_intervention(intervention_id)
            if inter:
                patch_data = (status, intervention_id)
                db.update_intervention_status(patch_data)
                return{"status": 200, "data":
                       [{"id": intervention_id, "message":
                        "Updated intervention record status"}]}, 200
            return{"message": "No record with id {} exists."
                   .format(intervention_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400


class Redflagstatus(Resource):
    def patch(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(id_pattern, id_string)
        if id_check:
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
            inter = db.get_redflag(intervention_id)
            if inter:
                patch_data = (status, red_flag_id)
                db.update_redflag_status(patch_data)
                return{"status": 200, "data":
                       [{"id": red_flag_id, "message":
                        "Updated redflag record status"}]}, 200
            return{"message": "No record with id {} exists."
                   .format(intervention_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400


class Protected(Resource):
    @jwt_required
    def get(self):
        return {"message": "Valid token,access granted"}
 