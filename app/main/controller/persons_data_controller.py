from flask import request
from flask_restplus import Resource

from ..util.dto import PersonsDataDto
from ..service.persons_data_service import create, get_all, get_one,update,delete,get_one_by_persons_id

api = PersonsDataDto.api
_person_data= PersonsDataDto.role


@api.route('/')
class PersonsDataList(Resource):
    @api.doc('list_of_registered_persons_data')
    @api.marshal_list_with(_person_data, envelope='data')
    def get(self):
        """List all registered persons data"""
        return get_all()

    @api.response(201, 'Person Data successfully created.')
    @api.doc('create a new person data')
    @api.expect(_person_data, validate=False)
    def post(self):
        """Creates a new person data """
        data = request.form
        return create(data=data)


@api.route('/<id>')
@api.param('id', 'The Person Data identifier')
@api.response(404, 'Person data not found.')
class PersonsData(Resource):
    @api.doc('get a person data')
    @api.marshal_with(_person_data)
    def get(self,id):
        """get a person given its identifier"""
        person = get_one(id=id)
        if not person:
            api.abort(404)
        else:
            return person
    
    @api.doc('update a person data')
    def put(self,id):
        """get a person data given its identifier and update"""
        data = request.json
        return update(id=id,data=data)
        
    
    @api.response(201, 'Person data successfully deleted')
    @api.doc('delete a person data')
    def delete(self,id):
        """get a person data given its identifier and delete"""
        return delete(id=id)

@api.route('/<id>/persons_id')
@api.param('id', 'The Person Data identifier')
@api.response(404, 'Person data not found.')
class PersonsBioData(Resource):
    @api.doc('get a person data by persons_id')
    @api.marshal_with(_person_data)
    def get(self,id):
        """get a person given its identifier"""
        person = get_one_by_persons_id(id=id)
        if not person:
            api.abort(404)
        else:
            return person