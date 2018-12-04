from flask_restful import Api, Resource
from flask import Blueprint

from .redflagviews import RedFlag
from .redflagviews import RedFlags
from .redflagviews import PatchLocation
from .redflagviews import PatchComment


version_one = Blueprint('api_v1', __name__, url_prefix = '/api/v1')
api = Api(version_one)

api.add_resource(RedFlag, '/red_flag/<int:red_flag_id>')
api.add_resource(RedFlags, '/red_flags')
api.add_resource(PatchLocation, '/red_flag/<int:red_flag_id>/location')
api.add_resource(PatchComment, '/red_flag/<int:red_flag_id>/comment')