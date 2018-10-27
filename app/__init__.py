# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.users_controller import api as user_ns
from .main.controller.verify_controller import api as verify_ns
from .main.controller.register_controller import api as register_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/users')
api.add_namespace(verify_ns, path='/verify')
api.add_namespace(register_ns, path='/register')
