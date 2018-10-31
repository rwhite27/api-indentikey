from .. import db, flask_bcrypt

class ResourceAccess(db.Model):
    """ Resource Access Model for storing resource access related details """
    __tablename__ = "resource_access"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_id = db.Column(db.Integer, unique=False, nullable=False)
    persons_id = db.Column(db.Integer, unique=False, nullable=False)
    is_active = db.Column(db.Integer, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    