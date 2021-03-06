import uuid
import datetime

from app.main import db
from app.main.model.users import Users


def save_new_user(data):
    user = Users.query.filter_by(email=data['email']).first()
    if not user:
        new_user = Users(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            registered_on = datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return Users.query.all()


def get_a_user(public_id):
    return Users.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()