from flask import request
from flask_restplus import Resource

from ..util.dto import ResourcesDto
from ..util.dto import ResourceAccessDto
from ..service.resources_service import create, get_all, get_one,update,delete, get_all_resouce_settings, get_all_resouce_access, put_resouce_settings,delete_all_resource_access

api = ResourcesDto.api
_resources= ResourcesDto.role
_resource_access = ResourceAccessDto.role


@api.route('/')
class PersonsList(Resource):
    @api.doc('list_of_registered_persons')
    @api.marshal_list_with(_resources, envelope='data')
    def get(self):
        """List all registered Resource Access"""
        return get_all()

    @api.response(201, 'Resource Access successfully created.')
    @api.doc('create a new Resource Access')
    @api.expect(_resources, validate=False)
    def post(self):
        """Creates a new Resource Access """
        data = request.form
        return create(data=data)


@api.route('/<id>')
@api.param('id', 'The Resource Access identifier')
@api.response(404, 'Resource Access not found.')
class Persons(Resource):
    @api.doc('get a person')
    @api.marshal_with(_resources)
    def get(self,id):
        """get a Resource Access given its identifier"""
        item = get_one(id=id)
        if not item:
            api.abort(404)
        else:
            return item
    
    @api.doc('update a Resource Access')
    @api.marshal_with(_resources)
    def put(self,id):
        """get a Resource Access given its identifier and update"""
        data = request.form
        return update(id=id,data=data)
        
    
    @api.response(201, 'Resource Access successfully deleted')
    @api.doc('delete a Resource Access')
    def delete(self,id):
        """get a Resource Access given its identifier and delete"""
        return delete(id=id)

@api.route('/<id>/resource-settings')
@api.param('id', 'The Resource Access identifier')
class ResourceSettings(Resource):
    @api.doc('get all the resource settings of a resouce')
    def get(self,id):
        return get_all_resouce_settings(id=id)
    
    @api.doc('get all the resource access of a resouce')
    def put(self,id):
        data = request.json
        return put_resouce_settings(id=id,data=data)

@api.route('/<id>/resource-access')
@api.param('id', 'The Resource identifier')
class ResourceAccess(Resource):
    @api.doc('get all the resource access of a resouce')
    def get(self,id):
        return get_all_resouce_access(id=id)

    @api.doc('get all the resource access of a resouce')
    def delete(self,id):
        return delete_all_resource_access(id=id)