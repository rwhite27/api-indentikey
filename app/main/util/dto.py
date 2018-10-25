from flask_restplus import Namespace, fields


class UsersDto:
    api = Namespace('users', description='user related operations')
    user = api.model('users', {
        'email': fields.String(required=True, description='user email address'),
        'public_id': fields.String(description='user Identifier')
    })

class OwnersDto:
    api = Namespace('owners', description='owners related operations')
    owner = api.model('owners', {
        'name': fields.String(required=True, description='owner name'),
        'username': fields.String(required=True, description='owner username'),
        'password': fields.String(required=True, description='owner password'),
        'public_id': fields.String(description='user Identifier')
    })

class VerifyDto:
    api = Namespace('verify', description='verification related operations')