import uuid
import datetime

from app.main import db
from app.main.model.persons_data import PersonsData


def create(data):

    new_item = PersonsData(
        persons_id=data['persons_id'],
        qr_code=data['qr_code'] if 'qr_code' in data else ' ',
        fingerprint=data['fingerprint'] if 'fingerprint' in data else ' ',
        face_model=data['face_model'] if 'face_model' in data else ' ',
        voice_profile=data['voice_profile'] if 'voice_profile' in data else ' ',
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_item)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 201


def get_all():
    return PersonsData.query.all()


def get_one(id):
    return PersonsData.query.filter_by(id=id).first()

def update(id,data):
    item = PersonsData.query.filter_by(id=id).first()
    if item:

        item.persons_id = data['persons_id']
        item.qr_code = data['qr_code'] if 'qr_code' in data else item.qr_code
        item.fingerprint = data['fingerprint'] if 'fingerprint' in data else item.fingerprint
        item.face_model = data['face_model'] if 'face_model' in data else item.face_model
        item.voice_profile = data['voice_profile'] if 'voice_profile' in data else item.voice_profile
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
    item = PersonsData.query.filter_by(id=id).first()
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