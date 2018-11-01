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
from flask import request
import numpy as np
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/ubuntu/api-indentikey/uploads'


def register_biometrics(settings,data):
    
    # for setting in settings:
    switcher={
                "QR_CODE":verify_qr_code(data=data),
                "FINGERPRINT":verify_fingerprint(data=data),
                "FACERECOG":register_face(data=data),
                "VOICERECOG": enroll_voice(data=data)
            }
    return switcher.get("FACERECOG","Invalid biometric setting")
    # user = Users.query.filter_by(email=data['email']).first()
    
def verify_qr_code(data):

    randomId = str(uuid.uuid4())

    persons_id = data['persons_id']

    return persons_id

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

    return True

    # #To send by email the generated qr code image.
    # fromaddr ="example@identikey.com"
    # toaddr = "rafaelwhite27@hotmail.com"
    # msg = MIMEMultipart()
    # msg['From'] = "example@identikey.com"
    # msg['To'] = "rafaelwhite27@hotmail.com"
    # msg['Subject'] = "QR Code Image Example"
    # body = "Python test mail"
    # msg.attach(MIMEText(body, 'plain'))

    # img_data = open('/home/thesis/api-indentikey/app/uploads/test.png', 'rb').read()
    # ImgFileName = 'test.png'
    # image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    # msg.attach(image)
    # # Here we create the actual mail server. It would be wise to create it for global use.
    # server = smtplib.SMTP('smtp.mailgun.org', 587)
    # server.ehlo()
    # server.starttls()
    # server.ehlo()
    # server.login("postmaster@sandbox42c331325cb141e9b02e8748f6bc2321.mailgun.org", "fc44fe896ab5732de5cc21ccdb9aff71-4836d8f5-57a231aa")
    # text = msg.as_string()
    # server.sendmail(fromaddr, toaddr, text)
    # server.quit()


def verify_fingerprint(data):
    # return Users.query.filter_by(public_id=public_id).first()
    return "No implementation yet"


def register_face(data):
   
    persons_id = data['persons_id']
    face = Face()
    # image = request.files['face']
    # face_image = image.read()
    # encoded_image = face_recognition.face_encodings(
    #             face_recognition.load_image_file('/home/ubuntu/api-indentikey/alexis5.jpg'))


    # Temporary save the image
    image = request.files['file']
    filename = secure_filename(image.filename)
    return image.save(os.path.join(UPLOAD_FOLDER, filename))


    encoded_image = face_recognition.face_encodings(
                face_recognition.load_image_file(face_image))
    
    encoded_image_array = np.array(encoded_image[0])
    encoded_image_string = ','.join(str(e) for e in encoded_image_array)

    return encoded_image_string

    # Lets save the id on the person's data
    person = Persons.query.filter_by(id=persons_id).first()

    if person:
        person_data = PersonsData.query.filter_by(persons_id=person.id).first()

        if person_data:
            person_data.face_model = encoded_image_string
            db.session.commit()
                
        else:
            return 'persons data not found'
    else:
        return 'person not found'
    
    return True

    #We need to saving the encoding to the encodings array


# Enrolls a newly created profile.
def enroll_voice(data):
     count = 0
     #Create first an enrollment profile
     profile_string = json.loads(create_voice_profile())

     if profile_string:

         profile_id = profile_string['verificationProfileId']
         #Now we save the profile string in our database. We may update the row, not create a new one, so we need to find by person's id
         
         persons_id = data['persons_id']

        # Lets save the id on the person's data
         person = Persons.query.filter_by(id=persons_id).first()

         if person:
            person_data = PersonsData.query.filter_by(persons_id=person.id).first()

            if person_data:
                person_data.voice_profile = profile_id
                db.session.commit()
                # enroll(profile_id)
                
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

# def enroll(profile_id):
#         #Create an enrollment. To enroll a person we need to enroll the voice 3 times.
#          headers = {
#             # Request headers
#             'Content-Type': 'multipart/form-data',
#             'Ocp-Apim-Subscription-Key': '9cad2c86ad8e4220ae02edc989424cac',
#          }

#          params = urllib.parse.urlencode({
#          })

#          #Lets enroll the person 3 times. We could use 3 diferent voice clips or just one.


#          # Here we open a 16k rate, 16 bit, mono WAV audio file. We need to check how files are received in flask.
#         #  body = open('/home/ubuntu/api-indentikey/rafaelp5_16k_16bit_mono.wav', 'rb')
#          recordings = request.files['recordings'][0]

#          return recordings

#          #Need to make 3 request per profile right here. We need to be able to handle 3 recording uploads
#          for recording in recordings:
#             body = recording.read()

#             conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
#             conn.request("POST", "/spid/v1.0/verificationProfiles/{}/enroll?%s".format(profile_id) %
#                     params, body, headers)
#             response = conn.getresponse()
#             data = response.read()
#             return data.decode('utf-8')
#             conn.close()