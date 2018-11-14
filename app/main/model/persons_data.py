from .. import db, flask_bcrypt

class PersonsData(db.Model):
    """ Persons Data Model for storing persons data related details """
    __tablename__ = "persons_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persons_id = db.Column(db.Integer, unique=False)
    qr_code = db.Column(db.String(100), unique=False, nullable=True)
    fingerprint = db.Column(db.String(200), unique=False, nullable=True)
    face_model = db.Column(db.Text(), unique=False, nullable=True)
    voice_profile = db.Column(db.String(100), unique=False, nullable=True)
    is_deleted = db.Column(db.Integer, unique=False,default=0,nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    