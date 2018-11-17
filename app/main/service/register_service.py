import uuid
import datetime
import pyqrcode
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import png
import os
import json
from app.main import db
from app.main.model.users import Users
import http.client, urllib.request, urllib.parse, urllib.error, base64
import face_recognition 
import numpy as np
from app.main.util.face import Face
from app.main.model.persons import Persons
from app.main.model.persons_data import PersonsData
from flask import jsonify
import base64
import numpy as np
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import requests
    
def register_qr_code(data):

    randomId = str(uuid.uuid4())

    persons_id = data['persons_id']

    # Lets save the id on the person's data
    person = Persons.query.filter_by(id=persons_id).first()

    if person:
        person_data = PersonsData.query.filter_by(persons_id=person.id).first()

        if person_data:
            person_data.qr_code = randomId
            db.session.commit()
        else:
            return 'persons data not found'
    else:
        return 'person not found'

    #Now we create the qr_code image
    qr = pyqrcode.create(randomId, error='L', version=5, mode='binary')

    #Then, we can either save or send it via email to the user.Maybe both and save the location of the qr_code on biometrics table.

    #To save the image in a new location on the server.
    qr.png('/home/ubuntu/api-indentikey/app/uploads/{}.png'.format(randomId), scale=5)

    return randomId

    # #To send by email the generated qr code image.
    # fromaddr ="example@identikey.com"
    # toaddr = "rafaelwhite27@hotmail.com"
    # msg = MIMEMultipart()
    # msg['From'] = "example@identikey.com"
    # msg['To'] = "rafaelwhite27@hotmail.com"
    # msg['Subject'] = "QR Code Image Example"
    # body = "Python test mail"
    # msg.attach(MIMEText(body, 'plain'))

    # img_data = open('/home/ubuntu/api-indentikey/app/uploads/{}.png'.format(randomId), 'rb').read()
    # ImgFileName = 'test.png'
    # image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    # msg.attach(image)
    # # Here we create the actual mail server. It would be wise to create it for global use.
    # server = smtplib.SMTP('smtp.mailgun.org', 587)
    # server.ehlo()
    # server.starttls()
    # server.ehlo()
    # server.login(os.getenv("MAILGUN_USERNAME"),os.getenv("MAILGUN_PASSWORD")) # Need to put this credential in a .env or some other file
    # text = msg.as_string()
    # server.sendmail(fromaddr, toaddr, text)
    # server.quit()


def register_fingerprint(data):
    persons_id = data['persons_id']

    count = 0

    while count < 3:
        image = data['fingerprint[{}]'.format(count)]
        filename = image.filename
        
        image.save(os.path.join('/home/ubuntu/api-indentikey/app/uploads','fingerprint[{}].bmp'.format(count)))
        filepath = '/home/ubuntu/api-indentikey/app/uploads/fingerprint[{}].bmp'.format(count)

        if (count == 0):
            fingerprint = filepath
        else:
            fingerprint = fingerprint + ',' + str(filepath)
        
        count += 1

    # Lets save the id on the person's data
    person = Persons.query.filter_by(id=persons_id).first()

    if person:
        person_data = PersonsData.query.filter_by(persons_id=person.id).first()

        if person_data:
            person_data.fingerprint = fingerprint
            db.session.commit()

            ##Send data to flask api here
            results = send_register_fingerprint(filename,persons_id)
            return results
                
        else:
            return 'persons data not found'
    else:
        return 'person not found'
    
    return True

def send_register_fingerprint(filename,persons_id):

    body_0 = open('/home/ubuntu/api-indentikey/app/uploads/fingerprint[0].bmp', 'rb')
    body_1 = open('/home/ubuntu/api-indentikey/app/uploads/fingerprint[1].bmp', 'rb')
    body_2 = open('/home/ubuntu/api-indentikey/app/uploads/fingerprint[2].bmp', 'rb')
    

    response = requests.post('http://ec2-52-21-122-184.compute-1.amazonaws.com:5000/register/{}'.format(persons_id),files=dict(fingerprint0=body_0,fingerprint1=body_1,fingerprint2=body_2))

    os.remove('/home/ubuntu/api-indentikey/app/uploads/fingerprint[0].bmp')
    os.remove('/home/ubuntu/api-indentikey/app/uploads/fingerprint[1].bmp')
    os.remove('/home/ubuntu/api-indentikey/app/uploads/fingerprint[2].bmp')


    return response


def register_face(data):
   
    persons_id = data['persons_id']
    face = Face()

    # Temporary save the image
    image = data['file']
    filename = image.filename
    image.save(os.path.join('/home/ubuntu/api-indentikey/app/uploads', filename))

    encoded_image = face_recognition.face_encodings(
                face_recognition.load_image_file('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename)))
    
    encoded_image_array = np.array(encoded_image[0])
    encoded_image_string = ','.join(str(e) for e in encoded_image_array)

    # Lets save the id on the person's data
    person = Persons.query.filter_by(id=persons_id).first()

    if person:
        person_data = PersonsData.query.filter_by(persons_id=person.id).first()

        if person_data:
            person_data.face_model = encoded_image_string
            db.session.commit()

            ##Send data to flask api here
            results = send_register_face(filename)
            os.remove('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename))
            return results
                
        else:
            return 'persons data not found'
    else:
        return 'person not found'
    
    return True

    #We need to saving the encoding to the encodings array

def send_register_face(filename):
    
    body = open('/home/ubuntu/api-indentikey/app/uploads/{}'.format(filename), 'rb')

    response = requests.post('http://ec2-52-21-122-184.compute-1.amazonaws.com:8080/register', files=dict(file=body))
    return response

# Enrolls a newly created profile.
def register_voice(data):
    
     #Create first an enrollment profile
     profile_string = json.loads(create_voice_profile())

     if profile_string:

         profile_id = profile_string['verificationProfileId']
         #Now we save the profile string in our database. We may update the row, not create a new one, so we need to find by person's id
         
         persons_id = data['persons_id']
         convert_audio_ogg(data)

        # Lets save the id on the person's data
         person = Persons.query.filter_by(id=persons_id).first()

         if person:
            person_data = PersonsData.query.filter_by(persons_id=person.id).first()

            if person_data:
                person_data.voice_profile = profile_id
                db.session.commit()
                return enroll(profile_id)
                
            else:
                return 'persons data not found'
         else:
            return 'person not found'
         
     else:
         return "New profile could not be created"  



#Creates a new enrollment profile
def create_voice_profile():
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '9cad2c86ad8e4220ae02edc989424cac',
    }

    params = urllib.parse.urlencode({
    })

    body = {
        "locale": "en-us",
    }

    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/spid/v1.0/verificationProfiles?%s" %
                 params, str(body), headers)
    response = conn.getresponse()
    voice_profile = response.read()
    return voice_profile.decode('utf-8')
    conn.close()

def enroll(profile_id):

        count = 0
        
        
        while count < 3:

             #Create an enrollment. To enroll a person we need to enroll the voice 3 times.
            headers = {
                # Request headers
                'Content-Type': 'multipart/form-data',
                'Ocp-Apim-Subscription-Key': '9cad2c86ad8e4220ae02edc989424cac',
            }

            params = urllib.parse.urlencode({
            })
            #Lets enroll the person 3 times. We could use 3 diferent voice clips or just one.
            # Here we open a 16k rate, 16 bit, mono WAV audio file. We need to check how files are received in flask.
            body = open('/home/ubuntu/api-indentikey/app/uploads/recordings[{}].wav'.format(count), 'rb')

            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/spid/v1.0/verificationProfiles/{}/enroll?%s".format(profile_id) %
                params, body, headers)
            response = conn.getresponse()
            data = response.read()
            confirmation = json.loads(data.decode('utf-8'))

            if 'enrollmentStatus' in confirmation:

                if(confirmation['enrollmentStatus'] == 'Enrolled'):
                    os.remove('/home/ubuntu/api-indentikey/app/uploads/recordings[{}].wav'.format(count))
                    return confirmation['enrollmentStatus']
                if(confirmation['enrollmentStatus'] == 'Enrolling'):
                    os.remove('/home/ubuntu/api-indentikey/app/uploads/recordings[{}].wav'.format(count))
            
            if 'error' in confirmation:
                
                if(confirmation['error']['message'] == 'TooNoisy'):
                    return confirmation['error']['message']
            
            conn.close()
            count += 1

def convert_audio_ogg(data):
     #We need to save the file first temporarily
     count = 0

     while count < 3:

         audio = data['recordings[{}]'.format(count)]
         filename = audio.filename
         audio.save(os.path.join('/home/ubuntu/api-indentikey/app/uploads','recordings[{}].ogg'.format(count)))

         #Convert Audio
         sound_ogg = AudioSegment.from_file('/home/ubuntu/api-indentikey/app/uploads/recordings[{}].ogg'.format(count), format="ogg")

         modify_frame_rate = sound_ogg.set_frame_rate(16000)

         modify_sample_width = modify_frame_rate.set_sample_width(2)

         modify_sample_width.export("/home/ubuntu/api-indentikey/app/uploads/recordings[{}].wav".format(count),format="wav")

         os.remove('/home/ubuntu/api-indentikey/app/uploads/recordings[{}].ogg'.format(count))
         count += 1