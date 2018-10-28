import uuid
import datetime
import pyqrcode

from app.main import db
from app.main.model.users import Users
import face_recognition
import os
import numpy as np



def verify(settings,data):
    
    #for setting in settings:
    switcher={
                "QR_CODE":verify_qr_code(data=data),
                "FINGERPRINT":verify_fingerprint(data=data),
                "FACERECOG":verify_face(data=data)
            }
    return switcher.get("FACERECOG","Invalid biometric setting")
    # user = Users.query.filter_by(email=data['email']).first()
    
def verify_qr_code(data):
    #return data['qr_code']
    return True
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

    #We dont need to store input data.

    alexis_test = face_recognition.face_encodings(
                face_recognition.load_image_file('/home/ubuntu/api-indentikey/alexis5.jpg'))

    return True


    # We are gonna encode all images here just for testing purposes
    encodings = []

    for image in os.listdir(path="/home/ubuntu/api-indentikey/all/"):
            try:
                encodings.append(face_recognition.face_encodings(
                    face_recognition.load_image_file(f"/home/ubuntu/api-indentikey/all/{image}"))[0])
            except Exception:
                continue

    encodings = np.array(encodings)

    face_recognition.compare_faces(encodings,alexis_test)

def verify_voice(data):
    db.session.add(data)
    db.session.commit()
