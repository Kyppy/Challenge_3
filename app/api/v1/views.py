import psycopg2
from flask import request
from flask_restful import Resource
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

