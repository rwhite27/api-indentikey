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
from subprocess import call

#Main function for qr_code verification
def verify_qr_code(data):
    
    qr_code = data['qr_code']

    person_data = PersonsData.query.filter_by(qr_code=qr_code).first()

    if person_data:
        if (person_data.qr_code == qr_code):
            person = Persons.query.filter_by(id=person_data.persons_id).first()
            response= {
                'persons_id': person.id,
                'persons_firstname': person.firstname,
                'persons_lastname': person.lastname
            }
            return response
        else:
            return False
    else:
        return 'Person Data not found related to this QR Code'

#Main function for fingerprint verification
def verify_fingerprint(data):
    
    # Temporary save the image
    image = data['finger_file']
    filename = image.filename
    image.save(os.path.join('/home/ubuntu/api-indentikey/app/uploads', filename))
    
    results = send_verify_fingerprint(filename)
    os.remove('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename))
    return results
                

def send_verify_fingerprint(filename):
    body = open('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename), 'rb')

    response = requests.post('http://ec2-52-21-122-184.compute-1.amazonaws.com:5000/verify', files=dict(file=body))
    return response.text


# Main function for face verification
def verify_face(data):
    
    # Temporary save the image
    image = data['face_file']
    filename = image.filename
    image.save(os.path.join('/home/ubuntu/api-indentikey/app/uploads', filename))
            
    results = send_verify_face(filename)
    os.remove('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename))
    return results
                
def send_verify_face(filename):
    body = open('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename), 'rb')

    response = requests.post('http://ec2-52-21-122-184.compute-1.amazonaws.com:8080/verify', files=dict(file=body))
    return response.text

#Main function for voice verification
def verify_voice(data,id):
    
    persons_id = id

    # Temporary save the image
    voice = data['voice_file']
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

    #command to convert from m4a to mp3
    filename_split = filename.split('.')[0]
    filename_extension = filename.split('.')[1]
    os.system('ffmpeg -i /home/ubuntu/api-indentikey/app/uploads/{}.{} /home/ubuntu/api-indentikey/app/uploads/{}.mp3'.format(filename_split,filename_extension,filename_split))

    #Convert Audio
    sound_ogg = AudioSegment.from_file('/home/ubuntu/api-indentikey/app/uploads/{}.mp3'.format(filename_split), format="mp3")

    modify_frame_rate = sound_ogg.set_frame_rate(16000)

    modify_sample_width = modify_frame_rate.set_sample_width(2)

    modify_sample_channel = modify_sample_width.set_channels(1)

    filename_split = filename.split('.')[0]
    modify_sample_channel.export("/home/ubuntu/api-indentikey/app/uploads/{}.wav".format(filename_split),format="wav")

    os.remove('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename))
    os.remove('/home/ubuntu/api-indentikey/app/uploads/{}.mp3'.format(filename_split))