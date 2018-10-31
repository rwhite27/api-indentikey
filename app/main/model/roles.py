from .. import db, flask_bcrypt

class Roles(db.Model):
    """ Roles Model for storing roles related details """
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    is_deleted = db.Column(db.Integer, unique=False,default=0,nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    