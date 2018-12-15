from flask import Flask, Blueprint
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token)
from .api.v1 import version_one as v1
import os


def create_app():
    app = Flask(__name__)
    # app.config.from_object(config[config_name])
    app.register_blueprint(v1)
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    jwt = JWTManager(app)    
    return app