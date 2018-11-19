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
        min_threshold=data['min_threshold'],
        code = str(uuid.uuid4()),
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_item)

    new_resource_access = ResourceAccess(
        resource_id=new_item.id,
        persons_id=data['persons_id'],
        roles_id=1,
        is_active=1,
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_resource_access)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.',
        'resource_id': new_item.id
    }
    return response_object, 201


def get_all():
    return Resources.query.all()


def get_one(id):
    return Resources.query.filter_by(id=id).first()

def update(id,data):
    item = Resources.query.filter_by(id=id).first()
    if item:

        item.name = data['name'] if 'name' in data else item.name
        item.main_resource_id = data['main_resource_id'] if 'main_resource_id' in data else item.main_resource_id
        item.min_threshold = data['min_threshold'] if 'min_threshold' in data else item.min_threshold
        item.is_deleted = data['is_deleted'] if 'is_deleted' in data else item.is_deleted
        item.persons_id=data['persons_id'] if 'persons_id' in data else item.persons_id
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

def delete_all_resource_access(id):
    resource = Resources.query.filter_by(id=id).first()
    if resource:
        resource_accesses = ResourceAccess.query.filter_by(resource_id=resource.id,is_deleted=0).all()
        if resource_accesses:
            for resource_access in resource_accesses:
                db.session.delete(resource_access)
                db.session.commit()
            
            resource_settings = ResourceSettings.query.filter_by(resources_id=resource.id,is_deleted=0).all()
            if resource_settings:
                for resource_setting in resource_settings:
                    db.session.delete(resource_setting)
                    db.session.commit()

            db.session.delete(resource)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully deleted'
            }
            return response_object, 201
        else:
            return False
    else:
        return 'No resource found'

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def get_all_resouce_settings(id):
    resource = Resources.query.filter_by(id=id).first()
    if resource:
        resource_settings = ResourceSettings.query.filter_by(resources_id=resource.id,is_deleted=0).all()
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

def put_resouce_settings(id,data):
    resource = Resources.query.filter_by(id=id).first()
    if resource:
        resource_settings = ResourceSettings.query.filter_by(resources_id=resource.id).all()
        if resource_settings:
            results = {}
            for resource_setting in resource_settings:
                method = VerificationMethods.query.filter_by(id=resource_setting.verification_methods_id).first()
                results[method.name] = resource_setting.threshold
                put_results = {}
                for (key,value) in results.items():
                    if key in data and data[key]== 0:
                        resource_setting.is_deleted = 1
                        db.session.commit()
                    elif key in data and data[key] > 0:
                        resource_setting.threshold = data[key]
                        resource_setting.is_deleted = 0
                        put_results[key] = data[key]
                        db.session.commit()
            return put_results
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