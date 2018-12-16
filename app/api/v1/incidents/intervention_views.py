import psycopg2
import re
from datetime import datetime
from datetime import timedelta
from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token,
                               get_jwt_identity)
from ..users import setup
from .incident_models import IncidentsDatabase
reg = setup.Regex()
db = IncidentsDatabase()
db.create_tables()
now = datetime.now()


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

    @jwt_required
    def post(self):
        data = request.get_json(silent=True)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        coordinates = re.match(reg.latlong_pattern, data["location"])
        if coordinates:
            if data['comment'] is None or data['comment'] is "":
                return{"message": "Intervention has "
                       "missing 'comment' field."}, 400
            if data['type'] == "Intervention":
                post_data = (data['type'], data['location'],
                             data['Images'], data['Videos'],
                             data['comment'], timestamp, get_jwt_identity())
                db.insert_intervention(post_data)
                _id = db.get_latest_id()
                return{"status": 201, "data": [{"id": _id[0], 
                       "message": "Created intervention record"}]}, 201
            return{"message": "Incident is not "
                   "type 'Intervention'."}, 400
        return{"status": 400, "message": "Location field is missing or "
                                         "formatted incorrectly.Please ensure "
                                         "it is formatted as a "
                                         "latitude-longitude coordinate "
                                         "e.g '15N,45E'."}, 400


class Intervention(Resource):
    def get(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            intervention_list = []
            if intervention_id is None or intervention_id is "":
                return{"message": "No incident id provided"}, 400
            inter = db.get_intervention(intervention_id)
            if inter:
                inter_data = {"id": inter[0], "createdOn": inter[1],
                              "createdBy": inter[2], "type": inter[3],
                              "location": inter[4], "status": inter[5],
                              "Images": inter[6], "Videos": inter[7],
                              "comment": inter[8]}
                intervention_list.append(inter_data)
                return {"status": 200, "data": intervention_list}, 200
            return{"message": "No intervention record with id {} exists."
                   .format(intervention_id)}, 404
        return {"status": 400, "message": "Invalid incident id in URL"}, 400

    @jwt_required
    def delete(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            if intervention_id is None or intervention_id is "":
                return{"message": "No incident id provided"}, 400
            inter = db.get_intervention(intervention_id)
            if inter:
                check_data = (intervention_id, get_jwt_identity())
                identity = db.check_user(check_data)
                if identity:
                    db.delete_record(intervention_id)
                    return {"status": 200, "data": [{"id": intervention_id,
                            "message": "Intervention record "
                                                    "has been deleted"}]}, 200
                return{"message": "Incident id associated with other account. "
                                  "Please select an incident id "
                                  "for one of your existing posts."}, 403
            return{"message": "No intervention record with id {} exists."
                   .format(intervention_id)}, 404
        return {"message": "Invalid incident id in URL"}, 400


class Interventionstatus(Resource):
    @jwt_required
    def patch(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            username = get_jwt_identity()
            valid = db.check_rank(username)
            if valid is False:
                return {"message": "You do not have permission "
                        "to access this route."}, 403
            incident_type = db.fetch_type(intervention_id)
            if incident_type != 'Intervention':
                return {"message": "Invalid incident type. "
                        "Please select an incident "
                        "of type 'Intervention.'"}, 400
            status = data["status"]
            if status != 'Resolved' and status != 'Rejected':
                return {"message": "Invalid update information"
                        "check your input and try again."}, 400
            inter = db.get_intervention(intervention_id)
            if inter:
                patch_data = (status, intervention_id)
                db.update_intervention_status(patch_data)
                return{"status": 200, "data":
                       [{"id": int(intervention_id), "message":
                        "Updated intervention record status"}]}, 200
            return{"message": "No record with id {} exists."
                   .format(intervention_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400


class UpdateInterventionLocation(Resource):
    @jwt_required
    def patch(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            coordinates = re.match(reg.latlong_pattern, data["location"])
            if coordinates:
                inter = db.get_intervention(intervention_id)
                if inter:
                    check_data = (intervention_id, get_jwt_identity())
                    identity = db.check_user(check_data)
                    if identity:
                        patch_data = (data["location"], intervention_id)
                        db.update_intervention_location(patch_data)
                        return{"status": 200, "data":
                               [{"id": intervention_id, "message": 
                                "Updated intervention "
                                 "record's location"}]}, 200
                    return{"message": "Incident id associated "
                           "with other user account. "
                           "Please select an incident id "
                           "for one of your existing posts."}, 403
                return{"message": "No record with id {} exists."
                       .format(intervention_id)}, 404
            return{"message": "Location field is formatted incorrectly."
                              "Please ensure it is formatted as a "
                              "latitude-longitude coordinate "
                              "e.g '15N,45E'."}, 400
        return {"message": "Bad credentials.Login failed"}, 400


class UpdateInterventionComment(Resource):
    @jwt_required
    def patch(self, intervention_id):
        id_string = str(intervention_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            comment = data["comment"]
            if comment is None or comment is "":
                return {"message": "Missing update information."
                        "Check your input and try again"}, 400
            inter = db.get_intervention(intervention_id)
            if inter:
                check_data = (intervention_id, get_jwt_identity())
                identity = db.check_user(check_data)
                if identity:
                    patch_data = (comment, intervention_id)
                    db.update_intervention_comment(patch_data)
                    return{"status": 200, "data":
                           [{"id": intervention_id, "message": 
                            "Updated intervention record comment"}]}, 200
                return{"message": "Incident id associated "
                       "with other account. "
                       "Please select an incident id "
                       "for one of your existing posts."}, 403
            return{"message": "No record with id {} exists."
                   .format(intervention_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400
