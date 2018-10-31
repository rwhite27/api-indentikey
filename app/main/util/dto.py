from flask_restplus import Namespace, fields


class UsersDto:
    api = Namespace('users', description='user related operations')
    user = api.model('users', {
        'email': fields.String(required=True, description='user email address'),
        'public_id': fields.String(description='user Identifier')
    })

class RolesDto:
    api = Namespace('roles', description='roles related operations')
    role = api.model('roles', {
        'id': fields.Integer(required=False, description='role id'),
        'name': fields.String(required=True, description='role name'),
        'is_deleted': fields.Integer(required=False, description='delete status'),
        'created_at': fields.DateTime(required=False, description=' when was created'),
        'updated_at': fields.DateTime(required=False, description='when was updated'),
    })

class PersonsDto:
    api = Namespace('persons', description='persons related operations')
    role = api.model('persons', {
        'id': fields.Integer(required=False, description='person id'),
        'role_id': fields.Integer(required=False, description='role id'),
        'firstname': fields.String(required=True, description='person firstname'),
        'lastname': fields.String(required=True, description='person lastname'),
        'email': fields.String(required=True, description='person email'),
        'password': fields.String(required=True, description='person password'),
        'is_deleted': fields.Integer(required=False, description='delete status'),
        'created_at': fields.DateTime(required=False, description=' when was created'),
        'updated_at': fields.DateTime(required=False, description='when was updated'),
    })

class PersonsDataDto:
    api = Namespace('persons-data', description='persons data related operations')
    role = api.model('persons-data', {
        'id': fields.Integer(required=False, description='person id'),
        'persons_id': fields.Integer(required=False, description='persons id'),
        'qr_code': fields.String(required=True, description='person qr_code'),
        'fingerprint': fields.String(required=True, description='person fingerprint'),
        'face_model': fields.String(required=True, description='person face_model'),
        'voice_profile': fields.String(required=True, description='person voice_profile'),
        'is_deleted': fields.Integer(required=False, description='delete status'),
        'created_at': fields.DateTime(required=False, description=' when was created'),
        'updated_at': fields.DateTime(required=False, description='when was updated'),
    })

class VerifyDto:
    api = Namespace('verify', description='verification related operations')

class RegisterDto:
    api = Namespace('register', description='registration related operations')