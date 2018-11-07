from flask import request
from flask_restplus import Resource

from ..util.dto import PersonsDto
from ..service.persons_service import create, get_all, get_one,update,delete
from flask_jwt import JWT, jwt_required, current_identity

api = PersonsDto.api
_person= PersonsDto.role


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
        data = request.json
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