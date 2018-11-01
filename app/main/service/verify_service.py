import uuid
import datetime
import pyqrcode

from app.main import db
from app.main.model.users import Users
import face_recognition
import os
import numpy as np
from flask import jsonify
from app.main.model.persons import Persons
from app.main.model.persons_data import PersonsData
from flask import request



def verify(settings,data,files):
    
    #for setting in settings:
    switcher={
                "QR_CODE":verify_qr_code(data=data),
                "FINGERPRINT":verify_fingerprint(data=data,files=files),
                "FACERECOG":verify_face(data=data,files=files)
            }
    return switcher.get("QR_CODE","Invalid biometric setting")
    # user = Users.query.filter_by(email=data['email']).first()
    
def verify_qr_code(data):
    
    persons_id = data['persons_id']

    person = Persons.query.filter_by(id=persons_id).first()

    if person:
        person_data = PersonsData.query.filter_by(persons_id=person.id).first()

        if person_data:
            if (person_data.qr_code == data['qr_code']):
                return True
            else:
                return False
                
        else:
            return 'persons data not found'
    else:
        return 'person not found'


def verify_fingerprint(data,files):
    # return Users.query.filter_by(public_id=public_id).first()
    return "No implementation yet"


def verify_face(data,files):

    persons_id = data['persons_id']
    #We dont need to store input data.

    # Temporary save the image
    image = files['file']
    filename = image.filename
    image.save(os.path.join('/home/ubuntu/api-indentikey/app/uploads', filename))

    encoded_image = face_recognition.face_encodings(
                face_recognition.load_image_file('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename)))

    # Lets save the id on the person's data
    person = Persons.query.filter_by(id=persons_id).first()

    if person:
        person_data = PersonsData.query.filter_by(persons_id=person.id).first()

        if person_data:
            #To convert saved string array to np array of floats
            face_model_array = person_data.face_model.split(',')
            face_model_np_array = np.array(face_model_array).astype(np.float)
            # back_to_np.astype(np.float)

            #it compares to a list of arrays. We need to make the comparison one to one---Todo-----
            face_recognition.compare_faces(face_model_np_array,encoded_image)
            os.remove('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename))
            return True
                
        else:
            return 'persons data not found'
    else:
        return 'person not found'
    
    return True

def verify_voice(data):
    db.session.add(data)
    db.session.commit()
