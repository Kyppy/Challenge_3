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

    
