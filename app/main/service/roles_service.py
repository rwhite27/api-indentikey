import uuid
import datetime

from app.main import db
from app.main.model.roles import Roles


def create(data):

    new_item = Roles(
        name=data['name'],
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_item)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 201


def get_all():
    return Roles.query.all()


def get_one(id):
    return Roles.query.filter_by(id=id).first()
def update(id,data):
    item = Roles.query.filter_by(id=id).first()
    if item:

        item.name = data['name']
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
        'message': 'Specific role does not exist'
        }
        return response_object, 201

def delete(id):
    item = Roles.query.filter_by(id=id).first()
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
        'message': 'Specific role does not exist'
        }
        return response_object, 201

def save_changes(data):
    db.session.add(data)
    db.session.commit()