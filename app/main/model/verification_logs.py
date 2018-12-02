from .. import db, flask_bcrypt

class VerificationLogs(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "verification_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    verification_status = db.Column(db.String(255), unique=False, nullable=False)
    resource_id = db.Column(db.Integer, unique=False,nullable=False)
    persons_id = db.Column(db.Integer, unique=False,nullable=False)
    is_deleted = db.Column(db.Integer, unique=False,default=0,nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)