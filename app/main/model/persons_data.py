from .. import db, flask_bcrypt

class PersonsData(db.Model):
    """ Persons Data Model for storing persons data related details """
    __tablename__ = "persons_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persons_id = db.Column(db.Integer, unique=False)
    qr_code = db.Column(db.String(100), unique=False, nullable=False)
    fingerprint = db.Column(db.String(200), unique=False, nullable=False)
    face_model = db.Column(db.Text(), unique=False, nullable=False)
    voice_profile = db.Column(db.String(100), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    