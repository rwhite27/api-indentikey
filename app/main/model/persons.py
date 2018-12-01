from .. import db, flask_bcrypt

class Persons(db.Model):
    """ Persons Model for storing persons related details """
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(64), unique=False, nullable=True)
    lastname = db.Column(db.String(64), unique=False, nullable=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), unique=False, nullable=False)
    was_validated = db.Column(db.Integer, unique=False,default=0,nullable=True)
    is_deleted = db.Column(db.Integer, unique=False,default=0,nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    