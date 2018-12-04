"""This module contains classes and methods that provide GET,POST,PATCH and DELETE requests for
the redflag incident records of the iReporter API"""
from flask import request
from flask_restful import Resource
from .redflagmodels import RedFlagModel

incidents = RedFlagModel()
""" List variable that acts as the record database"""
class RedFlag(Resource, RedFlagModel):
    """Contains resources for requests requiring individual/specific redflag incidents"""
    def get(self, red_flag_id):
        """Returns a specific redflag incident."""
        incident = next(filter(lambda x: x['id'] == red_flag_id, incidents.db), None)
        return {"status":200, "data":incident} if incident else\
        {"status":404, "message":"An incident with id '{}' does not exist.".format(red_flag_id)}
    def post(self, red_flag_id):
        """Post a single redflag incident and returns confirmation message."""
        data = request.get_json(silent=True)
        if data['id'] != red_flag_id:
            return {"message":"'id'{} of request body and 'id' {} of url do not match"\
                              .format(data['id'], red_flag_id)}, 400
        if next(filter(lambda x: x['id'] == red_flag_id, incidents.db), None):
            return {"message":"A red-flag with id '{}' already exists.".format(red_flag_id)}, 400
        incidents.store(data)
        return {"status":201, "data":{"id":red_flag_id, "message":"created red-flag record"}}
    def delete(self, red_flag_id):
        """Delete a single redflag incident"""
        incident = next(filter(lambda x: x['id'] == red_flag_id, incidents.db), None)
        if incident is None:
            return {"status":404, "message":\
                    "An incident with id '{}' does not exist."\
                    .format(red_flag_id)}
        incidents.db = list(filter(lambda x: x['id'] != red_flag_id, incidents.db))
        return {"status":200, "data":{"id":red_flag_id, "message":"red-flag record has been deleted"}} 
class RedFlags(Resource):
    """Contains resources for requests requiring all of the current redflag posts"""
    def get(self):
        """Returns all redflag records"""
        return{"status":200, "data":incidents.db} 
class PatchLocation(Resource):
    """Contains resources for requests that edit the 'location' field of a redflag record."""
    def patch(self, red_flag_id):
        """Edits the 'location' field of a single redflag record.Returns confirmation."""
        data = request.get_json(silent=True)
        if data['id'] != red_flag_id:
            return{"message":"'id'{} provided by request body and 'id' {} provided by url do not match"\
                    .format(data['id'], red_flag_id)}, 400
        incident = next(filter(lambda x: x['id'] == red_flag_id, incidents.db), None)
        if incident is None:
            return{"message":"A red-flag incident with id '{}' does not exist."\
            .format(red_flag_id)}, 404
        if data['location'] is None:
            return{"message":"Location update data was not provided."}, 404
        incident['location'] = data['location']
        return {"status":200, "data":{"id":red_flag_id, "message":"Updated red-flag record's location"}}
class PatchComment(Resource):
    """Contains resources for requests that edit the 'comment' field of a redflag record."""
    def patch(self, red_flag_id):
        """Edits the 'comment' field of a single redflag record.Returns confirmation."""
        data = request.get_json(silent=True)
        if data['id'] != red_flag_id:
            return{"message":"'id'{} of request body and 'id' {} of url do not match"\
                    .format(data['id'], red_flag_id)}, 400
        incident = next(filter(lambda x: x['id'] == red_flag_id, incidents.db), None)
        if incident is None:
            return{"message":"A red-flag incident with id '{}' does not exist.".format(red_flag_id)}, 404
        if data['comment'] is None:
            return{"message":"Comment update data was not provided."}, 400
        incident['comment'] = data['comment']
        return {"status":200, "data":{"id":red_flag_id, "message":"Updated red-flag record's comment"}}
