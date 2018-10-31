from flask import request
from flask_restplus import Resource

from ..util.dto import RolesDto
from ..service.roles_service import create, get_all, get_one,update,delete

api = RolesDto.api
_role= RolesDto.role


@api.route('/')
class RolesList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_role, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_role, validate=False)
    def post(self):
        """Creates a new User """
        data = request.json
        return create(data=data)


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class Roles(Resource):
    @api.doc('get a user')
    def get(self,id):
        """get a user given its identifier"""
        role = get_one(id=id)
        if not role:
            api.abort(404)
        else:
            return role
    
    @api.doc('update a role')
    def put(self,id):
        """get a user given its identifier and update"""
        data = request.json
        return update(id=id,data=data)
        
    
    @api.response(201, 'Role successfully deleted')
    @api.doc('delete a role')
    def delete(self,id):
        """get a user given its identifier and delete"""
        return delete(id=id)