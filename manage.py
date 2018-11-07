import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt import JWT, jwt_required, current_identity

from app.main import create_app, db
from app.main.model import users
from app.main.model import persons_data
from app.main.model import persons
from app.main.model import roles
from app.main.model import resource_access
from app.main.model import resources
from app.main.model import resource_settings
from app.main.model import verification_methods
from app import blueprint
from app.main.service.persons_service import authenticate, identity

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

jwt = JWT(app, authenticate, identity)

@manager.command
def run():
    app.run(host='0.0.0.0',port=8888)

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
