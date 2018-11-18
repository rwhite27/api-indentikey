import uuid
import datetime

from app.main import db
from app.main.model.resource_settings import ResourceSettings


def create(data):

    new_item = ResourceSettings(
        threshold=data['threshold'],
        resources_id=data['resources_id'],
        verification_methods_id=data['verification_methods_id'],
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_item)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 201


def get_all():
    return ResourceSettings.query.all()


def get_one(id):
    return ResourceSettings.query.filter_by(id=id).first()

def update(id,data):
    item = ResourceSettings.query.filter_by(id=id).first()
    if item:

        item.threshold = data['threshold'] if 'threshold' in data else item.threshold
        item.resources_id = data['resources_id'] if 'resources_id' in data else item.resources_id
        item.verification_methods_id = data['verification_methods_id'] if 'verification_methods_id' in data else item.verification_methods_id
        item.is_deleted = data['is_deleted'] if 'is_deleted' in data else item.is_deleted
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
    item = ResourceSettings.query.filter_by(id=id).first()
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