import uuid
import datetime
import pyqrcode

from app.main import db
from app.main.model.users import Users


def verify(settings,data):
    
    for setting in settings:
        switcher={
                    "QR_CODE":verify_qr_code(data=data),
                    "FINGERPRINT":verify_fingerprint(data=data)
                }
        return switcher.get(setting['biometric'],"Invalid biometric setting")
    # user = Users.query.filter_by(email=data['email']).first()
    
def verify_qr_code(data):
    return data['qr_code']

    #Search for persons qr code biometric data
    # person_biometric = Biometrics.query.filter_by(id=data['person_id'])
    if person_biometric:
        if person_biometric.qe_code == data['qr_code']:
            return True
        else:
            return False
    else:
        return "Person's biometric data not found"


def verify_fingerprint(data):
    # return Users.query.filter_by(public_id=public_id).first()
    return "No implementation yet"


def verify_face(data):
    db.session.add(data)
    db.session.commit()

def verify_voice(data):
    db.session.add(data)
    db.session.commit()