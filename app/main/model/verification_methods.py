from .. import db, flask_bcrypt

class VerificationMethods(db.Model):
    """ Verification Methods Model for storing verification methods related details """
    __tablename__ = "verification_methods"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    is_deleted = db.Column(db.Integer, unique=False,default=0, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)