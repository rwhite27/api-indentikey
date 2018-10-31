import uuid
import datetime

from app.main import db
from app.main.model.resource_access import ResourceAccess


def create(data):

    new_item = ResourceAccess(
        resource_id=data['resource_id'],
        persons_id=data['persons_id'],
        is_active=data['is_active'],
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_item)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 201


def get_all():
    return ResourceAccess.query.all()


def get_one(id):
    return ResourceAccess.query.filter_by(id=id).first()

def update(id,data):
    item = ResourceAccess.query.filter_by(id=id).first()
    if item:

        item.resource_id = data['resource_id']
        item.persons_id = data['persons_id']
        item.is_active = data['is_active']
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
    item = ResourceAccess.query.filter_by(id=id).first()
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