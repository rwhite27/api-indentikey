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


def register_biometrics(settings,data):
    
    # for setting in settings:
    switcher={
                "QR_CODE":verify_qr_code(data=data),
                "FINGERPRINT":verify_fingerprint(data=data)
            }
    return switcher.get("QR_CODE","Invalid biometric setting")
    # user = Users.query.filter_by(email=data['email']).first()
    
def verify_qr_code(data):

    randomId = str(uuid.uuid4())

    #we need to save the qr code by updating a recently created biometrics instance via its id. We are going to do this for every biometric registration.


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


def verify_face(data):
    db.session.add(data)
    db.session.commit()

def verify_voice(data):
    db.session.add(data)
    db.session.commit()