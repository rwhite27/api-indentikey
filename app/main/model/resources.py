from .. import db, flask_bcrypt

class Resources(db.Model):
    """ Resource Model for storing resource related details """
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    main_resource_id = db.Column(db.Integer, unique=False, nullable=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)