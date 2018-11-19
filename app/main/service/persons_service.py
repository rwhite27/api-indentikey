import uuid
import datetime

from app.main import db
from app.main.model.persons import Persons
from app.main.model.roles import Roles
from app.main.model.resources import Resources
from app.main.model.resource_access import ResourceAccess
from werkzeug.security import safe_str_cmp
from flask import session


def create(data):

    new_item = Persons(
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        password=data['password'],
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_item)
    return new_item.id


def get_all():
    return Persons.query.all()


def get_one(id):
    return Persons.query.filter_by(id=id).first()

def update(id,data):
    item = Persons.query.filter_by(id=id).first()
    if item:

        item.firstname = data['firstname']
        item.lastname = data['lastname']
        item.email = data['email']
        item.password = data['password']
        item.is_deleted = data['is_deleted']
        item.updated_at = datetime.datetime.utcnow()

        db.session.commit()

        response_object = {
        'status': 'success',
        'message': 'Successfully updated'
        }
        return response_object, 201
    else:
        response_object = {
        'status': 'failure',
        'message': 'Specific person does not exist'
        }
        return response_object, 201

def delete(id):
    item = Persons.query.filter_by(id=id).first()
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

def authenticate(username,password):
    user = Persons.query.filter_by(email=username).first()
    role = Roles.query.filter_by(id=user.roles_id).first()
    if user and role.name == 'Admin' and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return Persons.query.get(user_id)

def login(email,password):
    user = Persons.query.filter_by(email=email).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        session['id'] = user.id
        return user
    else:
        return False

def logout():
    session.pop('id',None)
    return True

def get_all_user_resources(id):
    resources = Resources.query.filter_by(persons_id=id).all()
    if resources:
        for resource in resources:
            results = []
            resource_access = ResourceAccess.query.filter_by(resource_id=resource.id).first()
            if resource_access:
                item = {}
                item['id'] = resource.id
                item['main_resource_id'] = resource.main_resource_id
                item['name'] = resource.name
                item['created_at'] = resource.created_at
                item['updated_at'] = resource.updated_at
                item['is_deleted'] = resource.is_deleted
                item['code'] = resource.code
                item['persons_id'] = resource.persons_id
                item['roles_id'] = resource_access.roles_id
                results.append(item)
            else:
                return 'No resource access found'
        return results
    else:
        return 'No resources found for that user'

def get_all_user_resource_access(id):
    resource_access = ResourceAccess.query.filter_by(persons_id=id,is_active=1).all()
    if resource_access:
        results = []
        for access in resource_access:
            resource = Resources.query.filter_by(id=access.resource_id).first()
            if resource:
                item = {}
                item['id'] = resource.id
                item['main_resource_id'] = resource.main_resource_id
                item['name'] = resource.name
                item['created_at'] = resource.created_at
                item['updated_at'] = resource.updated_at
                item['is_deleted'] = resource.is_deleted
                item['code'] = resource.code
                item['persons_id'] = resource.persons_id
                item['roles_id'] = access.roles_id
                results.append(item)
            else:
                item = {}
                item['roles_id'] = access.roles_id
                item['resource_id'] = access.resource_id
                item['persons_id'] = access.persons_id
                item['is_active'] = access.is_active
                item['created_at'] = access.created_at
                item['updated_at'] = access.updated_at
                results.append(item)
        return results
    else:
        return 'No resources found for that user'

def put_user_resource_access(id,data):
    resource_access = ResourceAccess.query.filter_by(persons_id=id,resource_id=data['resources_id']).first()
    if resource_access:
        resource_access.is_active = data['is_active']
        db.session.commit()
        
        response_object = {
        'status': 'success',
        'message': 'Successfully updated persons resource access'
        }
        return response_object, 201
    else:
        return "Resource Access for this persons not found"
        

def get_person_by_email(data):
    email = data['email']
    return Persons.query.filter_by(email=email).first()