import uuid
import datetime

from app.main import db
from app.main.model.persons import Persons
from app.main.model.roles import Roles
from app.main.model.resources import Resources
from werkzeug.security import safe_str_cmp
from flask import session


def create(data):

    new_item = Persons(
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        password=data['password'],
        roles_id=data['roles_id'],
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_item)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 201


def get_all():
    return Persons.query.all()


def get_one(id):
    return Persons.query.filter_by(id=id).first()

def update(id,data):
    item = Persons.query.filter_by(id=id).first()
    if item:

        item.roles_id = data['roles_id']
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
    role = Roles.query.filter_by(id=user.roles_id).first()
    if user and role.name == 'Admin' and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        session['id'] = user.id
        return user.id
    else:
        return False

def logout():
    session.pop('id',None)
    return True

def get_all_user_resources(id):
    resources = Resources.query.filter_by(persons_id=id).all()
    if resources:
        return resources
    else:
        return 'No resources found for that user'