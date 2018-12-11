from flask import Flask, Blueprint
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token)
from .api.v1 import version_one as v1


def create_app():
    app = Flask(__name__)
    app.register_blueprint(v1)
    app.config['JWT_SECRET_KEY'] = 'spongebob'
    jwt = JWTManager(app)
    return app