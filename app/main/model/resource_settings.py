from .. import db, flask_bcrypt

class ResourceSettings(db.Model):
    """ resource settings Model for storing rsource settings related details """
    __tablename__ = "resource_settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    verification_methods_id = db.Column(db.Integer, unique=False,nullable=False)
    resources_id = db.Column(db.Integer, unique=False, nullable=False)
    threshold = db.Column(db.Integer, unique=False, nullable=False)
    is_deleted = db.Column(db.Integer, unique=False,default=0, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)