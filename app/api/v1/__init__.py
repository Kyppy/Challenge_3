from flask_restful import Api, Resource
from flask import Blueprint

from .views import Interventions
from .views import Intervention
from .views import Signup

version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_one)

api.add_resource(Interventions, '/interventions')
api.add_resource(Intervention, '/intervention/<intervention_id>')
api.add_resource(Signup, '/auth/signup')
