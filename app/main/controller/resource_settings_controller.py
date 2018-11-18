from flask import request
from flask_restplus import Resource

from ..util.dto import ResourceSettingsDto
from ..service.resource_settings_service import create, get_all, get_one,update,delete

api = ResourceSettingsDto.api
_resource_settings= ResourceSettingsDto.role


@api.route('/')
class PersonsList(Resource):
    @api.doc('list_of_registered_persons')
    @api.marshal_list_with(_resource_settings, envelope='data')
    def get(self):
        """List all registered Resource Access"""
        return get_all()

    @api.response(201, 'Resource Access successfully created.')
    @api.doc('create a new Resource Access')
    @api.expect(_resource_settings, validate=False)
    def post(self):
        """Creates a new Resource Access """
        data = request.form
        return create(data=data)


@api.route('/<id>')
@api.param('id', 'The Resource Access identifier')
@api.response(404, 'Resource Access not found.')
class Persons(Resource):
    @api.doc('get a person')
    @api.marshal_with(_resource_settings)
    def get(self,id):
        """get a Resource Access given its identifier"""
        item = get_one(id=id)
        if not item:
            api.abort(404)
        else:
            return item
    
    @api.doc('update a Resource Access')
    def put(self,id):
        """get a Resource Access given its identifier and update"""
        data = request.form
        return update(id=id,data=data)
        
    
    @api.response(201, 'Resource Access successfully deleted')
    @api.doc('delete a Resource Access')
    def delete(self,id):
        """get a Resource Access given its identifier and delete"""
        return delete(id=id)