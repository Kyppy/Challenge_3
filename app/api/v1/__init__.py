from flask_restful import Api, Resource
from flask import Blueprint

from .incidents.redflag_views import Redflag, Redflags, Redflagstatus, \
                                      UpdateRedflagComment, \
                                      UpdateRedflagLocation
from .incidents.intervention_views import Intervention, Interventions, \
                                          Interventionstatus, \
                                          UpdateInterventionComment, \
                                          UpdateInterventionLocation
from .users.users_views import Signup, Login

version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_one)

api.add_resource(Interventions, '/interventions')
api.add_resource(Redflags, '/redflags')
api.add_resource(Intervention, '/intervention/<intervention_id>')
api.add_resource(Redflag, '/redflag/<redflag_id>')
api.add_resource(Signup, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(UpdateInterventionLocation,
                 '/interventions/<intervention_id>/location')
api.add_resource(UpdateRedflagLocation,
                 '/redflags/<redflag_id>/location')
api.add_resource(UpdateInterventionComment,
                 '/interventions/<int:intervention_id>/comment')
api.add_resource(UpdateRedflagComment,
                 '/redflags/<redflag_id>/comment')
api.add_resource(Interventionstatus,
                 '/interventions/<intervention_id>/status')
api.add_resource(Redflagstatus, '/redflags/<redflag_id>/status')
