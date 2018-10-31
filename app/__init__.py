# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.users_controller import api as user_ns
from .main.controller.verify_controller import api as verify_ns
from .main.controller.register_controller import api as register_ns

from .main.controller.roles_controller import api as roles_ns
from .main.controller.persons_controller import api as persons_ns
from .main.controller.persons_data_controller import api as persons_data_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/users')
api.add_namespace(verify_ns, path='/verify')
api.add_namespace(register_ns, path='/register')
api.add_namespace(roles_ns, path='/roles')
api.add_namespace(persons_ns, path='/persons')
api.add_namespace(persons_data_ns, path='/persons-data')
