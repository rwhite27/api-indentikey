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
import json
from pydub import AudioSegment
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests



def verify(settings,data):
    
    #Poner el switch en el controller en vez de en el servicio
    #for setting in settings:
    switcher={
                "QR_CODE":verify_qr_code(data=data),
                "FINGERPRINT":verify_fingerprint(data=data),
                "FACERECOG":verify_face(data=data),
                "VOICERECOG":verify_voice(data=data)
            }
    return switcher.get("FINGERPRINT","Invalid biometric setting")
    # user = Users.query.filter_by(email=data['email']).first()
    
def verify_qr_code(data):
    return 'hello'
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


def verify_fingerprint(data):
    persons_id = data['persons_id']
    #We dont need to store input data.

    # Temporary save the image
    image = data['file']
    filename = image.filename
    image.save(os.path.join('/home/ubuntu/api-indentikey/app/uploads', filename))

    # Lets save the id on the person's data
    person = Persons.query.filter_by(id=persons_id).first()

    if person:
        person_data = PersonsData.query.filter_by(persons_id=person.id).first()

        if person_data:
            #it compares to a list of arrays. We need to make the comparison one to one---Todo-----
            results = send_verify_fingerprint(filename,persons_id)
            os.remove('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename))
            return results
                
        else:
            return 'persons data not found'
    else:
        return 'person not found'
    
    return True

def send_verify_fingerprint(filename,persons_id):
    body = open('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename), 'rb')

    response = requests.post('http://ec2-52-21-122-184.compute-1.amazonaws.com:5000/verify/{}'.format(persons_id), files=dict(file=body))
    return response


def verify_face(data):
    return 'hello'
    persons_id = data['persons_id']
    #We dont need to store input data.

    # Temporary save the image
    image = data['file']
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
            results = send_verify_face(filename)
            os.remove('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename))
            return results
                
        else:
            return 'persons data not found'
    else:
        return 'person not found'
    
    return True

def send_verify_face(filename):
    body = open('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename), 'rb')

    response = requests.post('http://ec2-52-21-122-184.compute-1.amazonaws.com:8080/verify', files=dict(file=body))
    return response


def verify_voice(data):
    return 'hello'
    persons_id = data['persons_id']

    # Temporary save the image
    voice = data['file']
    filename = voice.filename
    voice.save(os.path.join('/home/ubuntu/api-indentikey/app/uploads', filename))

    convert_audio_ogg(filename)

    person = Persons.query.filter_by(id=persons_id).first()

    if person:
        person_data = PersonsData.query.filter_by(persons_id=person.id).first()

        if person_data:
            return verify_azure(person_data.voice_profile,filename)
        else:
            return 'persons data not found'
    else:
        return 'person not found'

def verify_azure(profile_id,filename):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '9cad2c86ad8e4220ae02edc989424cac',
    }

    params = urllib.parse.urlencode({
    })

    filename_split = filename.split('.')[0]
    body = open('/home/ubuntu/api-indentikey/app/uploads/{}.wav'.format(filename_split), 'rb')

    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/spid/v1.0/verify?verificationProfileId={}&{}".format(profile_id,params),body, headers)
    response = conn.getresponse()
    data = response.read()
    confirmation = json.loads(data.decode('utf-8'));

    if 'result' in confirmation:
        if(confirmation['result'] == 'Accept'):
            os.remove('/home/ubuntu/api-indentikey/app/uploads/{}.wav'.format(filename_split))
            return True
        if(confirmation['result'] == 'Reject'):
            os.remove('/home/ubuntu/api-indentikey/app/uploads/{}.wav'.format(filename_split))
            return False

    conn.close()

def convert_audio_ogg(filename):

    #Convert Audio
    sound_ogg = AudioSegment.from_file('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename), format="ogg")

    modify_frame_rate = sound_ogg.set_frame_rate(16000)

    modify_sample_width = modify_frame_rate.set_sample_width(2)

    filename_split = filename.split('.')[0]
    modify_sample_width.export("/home/ubuntu/api-indentikey/app/uploads/{}.wav".format(filename_split),format="wav")

    os.remove('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename))