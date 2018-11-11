import uuid
import datetime

from app.main import db
from app.main.model.resources import Resources
from app.main.model.resource_settings import ResourceSettings
from app.main.model.resource_access import ResourceAccess
from app.main.model.persons import Persons
from app.main.model.verification_methods import VerificationMethods



def create(data):

    new_item = Resources(
        name=data['name'],
        main_resource_id=data['main_resource_id'],
        persons_id=data['persons_id'],
        code = str(uuid.uuid4()),
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_item)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 201


def get_all():
    return Resources.query.all()


def get_one(id):
    return Resources.query.filter_by(id=id).first()

def update(id,data):
    item = Resources.query.filter_by(id=id).first()
    if item:

        item.name = data['name']
        item.main_resource_id = data['main_resource_id']
        item.is_deleted = data['is_deleted']
        item.persons_id=data['persons_id'],
        item.updated_at = datetime.datetime.utcnow()

        db.session.commit()

        return item
    else:
        response_object = {
        'status': 'failure',
        'message': 'Specific person does not exist'
        }
        return response_object, 201

def delete(id):
    item = Resources.query.filter_by(id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        response_object = {
        'status': 'success',
        'message': 'Successfully deleted'
        }
        return response_object, 201
    else:
        response_object = {
        'status': 'failure',
        'message': 'Specific person does not exist'
        }
        return response_object, 201

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def get_all_resouce_settings(id):
    resource = Resources.query.filter_by(id=id).first()
    if resource:
        resource_settings = ResourceSettings.query.filter_by(resources_id=resource.id).all()
        if resource_settings:
            results = {}
            for resource_setting in resource_settings:
                method = VerificationMethods.query.filter_by(id=resource_setting.verification_methods_id).first()
                results[method.name] = resource_setting.threshold
            
            return results
        else:
            return False
    else:
        return 'No resource found'

def get_all_resouce_access(id):
    resource = Resources.query.filter_by(id=id).first()
    if resource:
        resource_access = ResourceAccess.query.filter_by(resource_id=resource.id).all()
        if resource_access:
            results = []
            for access in resource_access:
                person = Persons.query.filter_by(id=access.persons_id).first()
                item = {}
                item['id'] = access.id
                item['resource_id'] = access.resource_id
                item['persons_id'] = person.id
                item['persons_firstname'] = person.firstname
                item['persons_lastname'] = person.lastname
                item['persons_email'] = person.email
                item['is_active'] = access.is_active
                item['is_deleted'] = access.is_deleted
                item['created_at'] = access.created_at
                item['updated_at'] = access.updated_at

                results.append(item)
            return results
        else:
            return "No resource access found"
    else:
        return 'No resource found'