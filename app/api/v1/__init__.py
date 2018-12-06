from flask_restful import Api, Resource
from flask import Blueprint

from .views import Interventions
from .views import Intervention
from .views import Signup
from .views import Login
from .views import Updatelocation
from .views import Updatecomment
from .views import Interventionstatus
from .views import Redflagstatus


version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_one)

api.add_resource(Interventions, '/interventions')
api.add_resource(Intervention, '/intervention/<int:intervention_id>')
api.add_resource(Signup, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(Updatelocation,
                 '/interventions/<int:intervention_id>/location')
api.add_resource(Updatecomment, '/interventions/<int:intervention_id>/comment')
api.add_resource(Interventionstatus,
                 '/interventions/<int:intervention_id>/status')
api.add_resource(Redflagstatus, '/red_flags/<int:red_flag_id>/status')
