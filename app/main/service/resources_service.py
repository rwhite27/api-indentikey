import uuid
import datetime

from app.main import db
from app.main.model.resources import Resources


def create(data):

    new_item = Resources(
        name=data['name'],
        main_resource_id=data['main_resource_id'],
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