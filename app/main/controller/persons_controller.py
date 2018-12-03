from flask import request
from flask_restplus import Resource

from ..util.dto import PersonsDto
from ..util.dto import ResourcesDto
from ..service.persons_service import create, get_all, get_one,update,delete, login,logout,get_all_user_resources, get_person_by_email,get_all_user_resource_access, put_user_resource_access,validate_persons_email,add_invite_to_resource,send_invitation
from flask_jwt import JWT, jwt_required, current_identity

api = PersonsDto.api
_person= PersonsDto.role
_resource = ResourcesDto.role


@api.route('/')
class PersonsList(Resource):
    @api.doc('list_of_registered_persons')
    @jwt_required()
    @api.marshal_list_with(_person, envelope='data')
    def get(self):
        """List all registered persons"""
        return get_all()

    @api.response(201, 'Person successfully created.')
    @api.doc('create a new person')
    @api.expect(_person, validate=False)
    def post(self):
        """Creates a new person """
        data = request.form
        return create(data=data)


@api.route('/<id>')
@api.param('id', 'The Person identifier')
@api.response(404, 'Person not found.')
class Persons(Resource):
    @api.doc('get a person')
    @api.marshal_with(_person)
    def get(self,id):
        """get a person given its identifier"""
        person = get_one(id=id)
        if not person:
            api.abort(404)
        else:
            return person
    
    @api.doc('update a role')
    def put(self,id):
        """get a person given its identifier and update"""
        data = request.json
        return update(id=id,data=data)
        
    
    @api.response(201, 'Person successfully deleted')
    @api.doc('delete a person')
    def delete(self,id):
        """get a person given its identifier and delete"""
        return delete(id=id)


@api.route('/login')
class PersonsLogin(Resource):
    @api.doc('Login')
    @api.marshal_list_with(_person)
    def post(self):
        """Login User"""
        data = request.form
        return login(data['email'],data['password'])

@api.route('/logout')
class PersonsLogout(Resource):
    @api.doc('Logout')
    def post(self):
        """List all registered persons"""
        return logout()

@api.route('/<id>/resources')
class PersonsLogout(Resource):
    @api.doc('Logout')
    def get(self,id):
        """List all registered persons"""
        return get_all_user_resources(id=id)

@api.route('/<id>/resources-access')
class PersonsLogout(Resource):
    @api.doc('Logout')
    def get(self,id):
        """List all registered persons"""
        return get_all_user_resource_access(id=id)
    
    def put(self,id):
        """List all registered persons"""
        data = request.form
        return put_user_resource_access(id=id,data=data)

@api.route('/email')
class PersonsLogout(Resource):
    @api.doc('Get person by email')
    @api.marshal_list_with(_person)
    def post(self):
        data = request.form
        """Fetch a person by email"""
        return get_person_by_email(data)

@api.route('/validate')
class PersonsValidate(Resource):
    @api.doc('validate a persons through email')
    def get(self):
        email = request.args.get('email')
        """List all registered persons"""
        return validate_persons_email(email=email)

@api.route('/invite/<id>/resource')
class PersonsInvite(Resource):
    @api.doc('validate a persons through email')
    def get(self,id):
        email = request.args.get('email')
        resource_id = request.args.get('resource_id')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        """List all registered persons"""
        return add_invite_to_resource(email=email,resource_id=resource_id,from_date=from_date,to_date=to_date)

    def post(self,id):
        data = request.form
        """Fetch a person by email"""
        return send_invitation(id=id,data=data)