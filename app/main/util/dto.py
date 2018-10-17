from flask_restplus import Namespace, fields


class UsersDto:
    api = Namespace('users', description='user related operations')
    user = api.model('users', {
        'email': fields.String(required=True, description='user email address'),
        'public_id': fields.String(description='user Identifier')
    })