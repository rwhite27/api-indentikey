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
from app.main.util import Face


def register_biometrics(settings,data):
    
    # for setting in settings:
    switcher={
                "QR_CODE":verify_qr_code(data=data),
                "FINGERPRINT":verify_fingerprint(data=data),
                "FACERECOG":'hello',
                "VOICERECOG": enroll_voice(data=data)
            }
    return switcher.get("VOICERECOG","Invalid biometric setting")
    # user = Users.query.filter_by(email=data['email']).first()
    
def verify_qr_code(data):

    return "hello"

    randomId = str(uuid.uuid4())

    #Now we create the qr_code image
    qr = pyqrcode.create(randomId, error='L', version=5, mode='binary')

    #Then, we can either save or send it via email to the user.Maybe both and save the location of the qr_code on biometrics table.

    #To save the image in a new location on the server.
    qr.png('/home/thesis/api-indentikey/app/uploads/test.png', scale=5)

    #To send by email the generated qr code image.
    fromaddr ="example@identikey.com"
    toaddr = "rafaelwhite27@hotmail.com"
    msg = MIMEMultipart()
    msg['From'] = "example@identikey.com"
    msg['To'] = "rafaelwhite27@hotmail.com"
    msg['Subject'] = "QR Code Image Example"
    body = "Python test mail"
    msg.attach(MIMEText(body, 'plain'))

    img_data = open('/home/thesis/api-indentikey/app/uploads/test.png', 'rb').read()
    ImgFileName = 'test.png'
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)
    # Here we create the actual mail server. It would be wise to create it for global use.
    server = smtplib.SMTP('smtp.mailgun.org', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("postmaster@sandbox42c331325cb141e9b02e8748f6bc2321.mailgun.org", "fc44fe896ab5732de5cc21ccdb9aff71-4836d8f5-57a231aa")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def verify_fingerprint(data):
    # return Users.query.filter_by(public_id=public_id).first()
    return "No implementation yet"


def register_face(data):
   
    face = Face()
    face.generate_encodes('path/to/file')

    #We need to saving the encoding to the encodings array


# Enrolls a newly created profile.
def enroll_voice(data):
     
     #Create first an enrollment profile
     profile_string = json.loads(create_voice_profile())

     if profile_string:

         profile_id = profile_string['verificationProfileId']
         #Now we save the profile string in our database. We may update the row, not create a new one, so we need to find by person's id

         
         
         #-------------------TODO-----------------------------
         #Create an enrollment. To enroll a person we need to enroll the voice 3 times.
         headers = {
            # Request headers
            'Content-Type': 'multipart/form-data',
            'Ocp-Apim-Subscription-Key': '9cad2c86ad8e4220ae02edc989424cac',
         }

         params = urllib.urlencode({
         })

         #Lets enroll the person 3 times. We could use 3 diferent voice clips or just one.


         # Here we open a 16k rate, 16 bit, mono WAV audio file. We need to check how files are received in flask.
         body = open('test/valentina/Wavs/valentina_a_1.wav', 'rb')

         conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
         conn.request("POST", "/spid/v1.0/verificationProfiles/{profile_id}/enroll?%s" %
                 params, body, headers)
         response = conn.getresponse()
         data = response.read()
         return data
         conn.close()


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

