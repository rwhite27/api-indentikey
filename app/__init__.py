# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.users_controller import api as user_ns
from .main.controller.verify_controller import api as verify_ns
from .main.controller.register_controller import api as register_ns

from .main.controller.roles_controller import api as roles_ns
from .main.controller.persons_controller import api as persons_ns
from .main.controller.persons_data_controller import api as persons_data_ns
from .main.controller.resource_access_controller import api as resource_access_ns
from .main.controller.resource_settings_controller import api as resource_settings_ns
from .main.controller.resources_controller import api as resources_ns
from .main.controller.verification_methods_controller import api as verification_methods_ns

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
api.add_namespace(resource_access_ns, path='/resource-access')
api.add_namespace(resource_settings_ns, path='/resource-settings')
api.add_namespace(resources_ns, path='/resources')
api.add_namespace(verification_methods_ns, path='/verification-methods')
