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

    @jwt_required
    def post(self):
        data = request.get_json(silent=True)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        coordinates = re.match(reg.latlong_pattern, data["location"])
        if coordinates:
            if data['comment'] is None or data['comment'] is "":
                return{"message": "Redflag has missing 'comment' field."}, 400
            if data['type'] == "Redflag":
                post_data = (data['type'], data['location'],
                             data['Images'], data['Videos'],
                             data['comment'], timestamp, get_jwt_identity())
                db.insert_intervention(post_data)
                _id = db.get_latest_id()
                return{"status": 201, "data": [{"id": _id[0],
                       "message": "Created redflag record"}]}, 201
            return{"message": "Incident is not "
                   "type 'Redflag'."}, 400
        return{"message": "Location field is missing or formatted "
                          "incorrectly.Please ensure it is formatted as a "
                          "latitude-longitude coordinate e.g '15N,45E'."}, 400


class Redflag(Resource):
    def get(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            redflag_list = []
            if redflag_id is None or redflag_id is "":
                return{"message": "No incident id provided"}, 400
            red = db.get_redflag(redflag_id)
            if red:
                red_data = {"id": red[0], "createdOn": red[1],
                            "createdBy": red[2], "type": red[3],
                            "location": red[4], "status": red[5],
                            "Images": red[6], "Videos": red[7],
                            "comment": red[8]}
                redflag_list.append(red_data)
                return {"status": 200, "data": redflag_list}, 200
            return{"message": "No redflag record with id {} exists."
                   .format(redflag_id)}, 404
        return {"message": "Invalid incident id in URL"}, 400

    @jwt_required
    def delete(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            if redflag_id is None or redflag_id is "":
                return{"message": "No incident id provided"}, 400
            red = db.get_redflag(redflag_id)
            if red:
                check_data = (redflag_id, get_jwt_identity())
                identity = db.check_user(check_data)
                if identity:
                    db.delete_record(redflag_id)
                    return {"status": 200, "data": [{"id": redflag_id,
                            "message": "Redflag record "
                                                    "has been deleted"}]}, 200
                return{"message": "Incident id associated with other account. "
                                  "Please select an incident id "
                                  "for one of your existing posts."}, 403
            return{"message": "No redflag record with id {} exists."
                   .format(redflag_id)}, 404
        return {"message": "Invalid incident id in URL"}, 400


class Redflagstatus(Resource):
    @jwt_required
    def patch(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            username = get_jwt_identity()
            valid = db.check_rank(username)
            if valid is False:
                return {"message": "You do not have permission "
                        "to access this route."}, 403
            incident_type = db.fetch_type(redflag_id)
            if incident_type != 'Redflag':
                return {"message": "Invalid incident type. "
                        "Please select an incident of type 'Redflag'."}, 400
            status = data["status"]
            if status != 'Resolved' and status != 'Rejected':
                return {"message": "Invalid update information"
                        "check your input and try again."}, 400
            red = db.get_redflag(redflag_id)
            if red:
                patch_data = (status, redflag_id)
                db.update_redflag_status(patch_data)
                return{"status": 200, "data":
                       [{"id": int(redflag_id), "message":
                        "Updated redflag record status"}]}, 200
            return{"message": "No record with id {} exists."
                   .format(redflag_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400


class UpdateRedflagLocation(Resource):
    @jwt_required
    def patch(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            coordinates = re.match(reg.latlong_pattern, data["location"])
            if coordinates:
                inter = db.get_redflag(redflag_id)
                if inter:
                    check_data = (redflag_id, get_jwt_identity())
                    identity = db.check_user(check_data)
                    if identity:
                        patch_data = (data["location"], redflag_id)
                        db.update_intervention_location(patch_data)
                        return{"status": 200, "data":
                               [{"id": redflag_id, "message":
                                "Updated redflag record's location"}]}, 200
                    return{"message": "Incident id associated "
                           "with other account. "
                           "Please select an incident id "
                           "for one of your existing posts."}, 403
                return{"message": "No record with id {} exists."
                       .format(redflag_id)}, 404
            return{"message": "Location field is formatted incorrectly."
                              "Please ensure it is formatted as a "
                              "latitude-longitude coordinate "
                              "e.g '15N,45E'."}, 400
        return {"message": "Bad credentials.Login failed"}, 400


class UpdateRedflagComment(Resource):
    @jwt_required
    def patch(self, redflag_id):
        id_string = str(redflag_id)
        id_check = re.match(reg.id_pattern, id_string)
        if id_check:
            data = request.get_json(silent=True)
            comment = data["comment"]
            if comment is None or comment is "":
                return {"message": "Missing update information"
                        "check your input and try again"}, 400
            inter = db.get_redflag(redflag_id)
            if inter:
                check_data = (redflag_id, get_jwt_identity())
                identity = db.check_user(check_data)
                if identity:
                    patch_data = (comment, redflag_id)
                    db.update_intervention_comment(patch_data)
                    return{"status": 200, "data":
                           [{"id": redflag_id, "message":
                            "Updated redflag record comment"}]}, 200
                return{"message": "Incident id associated "
                       "with other account. "
                       "Please select an incident id "
                       "for one of your existing posts."}, 403
            return{"message": "No record with id {} exists."
                   .format(redflag_id)}, 404
        return {"message": "Bad credentials.Login failed"}, 400