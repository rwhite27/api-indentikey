import uuid
import datetime

from app.main import db
from app.main.model.persons import Persons
from app.main.model.roles import Roles
from app.main.model.resources import Resources
from app.main.model.resource_access import ResourceAccess
from werkzeug.security import safe_str_cmp
from flask import session
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import os


def create(data):

    new_item = Persons(
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        password=data['password'],
        was_validated = 0,
        created_at = datetime.datetime.utcnow()
    )
    save_changes(new_item)
    send_validation_email(data['email'])

    #Entonces aqui deberiamos enviar el mensaje de checkiar el email para validar su cuenta en vez del id.
    # response_object = {
    #     'status': 'success',
    #     'message': 'Successfully updated'
    #     }
    # return response_object, 201
    return new_item.id


def get_all():
    return Persons.query.all()


def get_one(id):
    return Persons.query.filter_by(id=id).first()

def update(id,data):
    item = Persons.query.filter_by(id=id).first()
    if item:

        item.firstname = data['firstname']
        item.lastname = data['lastname']
        item.email = data['email']
        item.password = data['password']
        item.is_deleted = data['is_deleted']
        item.updated_at = datetime.datetime.utcnow()

        db.session.commit()

        response_object = {
        'status': 'success',
        'message': 'Successfully updated'
        }
        return response_object, 201
    else:
        response_object = {
        'status': 'failure',
        'message': 'Specific person does not exist'
        }
        return response_object, 201

def delete(id):
    item = Persons.query.filter_by(id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        response_object = {
        'status': 'success',
        'message': 'Successfully deleted'
        }
        return response_object, 201
    else:
        response_object = {
        'status': 'failure',
        'message': 'Specific person does not exist'
        }
        return response_object, 201

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def authenticate(username,password):
    user = Persons.query.filter_by(email=username).first()
    role = Roles.query.filter_by(id=user.roles_id).first()
    if user and role.name == 'Admin' and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return Persons.query.get(user_id)

def login(email,password):
    user = Persons.query.filter_by(email=email,was_validated=1).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        session['id'] = user.id
        return user
    else:
        return False

def logout():
    session.pop('id',None)
    return True

def get_all_user_resources(id):
    resources = Resources.query.filter_by(persons_id=id).all()
    if resources:
        for resource in resources:
            results = []
            resource_access = ResourceAccess.query.filter_by(resource_id=resource.id).first()
            if resource_access:
                item = {}
                item['id'] = resource.id
                item['main_resource_id'] = resource.main_resource_id
                item['name'] = resource.name
                item['created_at'] = resource.created_at
                item['updated_at'] = resource.updated_at
                item['is_deleted'] = resource.is_deleted
                item['code'] = resource.code
                item['persons_id'] = resource.persons_id
                item['roles_id'] = resource_access.roles_id
                results.append(item)
            else:
                return 'No resource access found'
        return results
    else:
        return 'No resources found for that user'

def get_all_user_resource_access(id):
    resource_access = ResourceAccess.query.filter_by(persons_id=id,is_active=1).all()
    if resource_access:
        results = []
        for access in resource_access:
            resource = Resources.query.filter_by(id=access.resource_id).first()
            if resource:
                item = {}
                item['id'] = resource.id
                item['main_resource_id'] = resource.main_resource_id
                item['name'] = resource.name
                item['created_at'] = resource.created_at
                item['updated_at'] = resource.updated_at
                item['is_deleted'] = resource.is_deleted
                item['code'] = resource.code
                item['persons_id'] = resource.persons_id
                item['roles_id'] = access.roles_id

                if resource.main_resource_id > 0:
                    main_resource = Resources.query.filter_by(id=resource.main_resource_id).first()
                    if main_resource:
                        item['main_resource_name'] = main_resource.name

                results.append(item)
            else:
                item = {}
                item['roles_id'] = access.roles_id
                item['resource_id'] = access.resource_id
                item['persons_id'] = access.persons_id
                item['is_active'] = access.is_active
                item['created_at'] = access.created_at
                item['updated_at'] = access.updated_at
                results.append(item)
        return results
    else:
        return 'No resources found for that user'

def put_user_resource_access(id,data):
    resource_access = ResourceAccess.query.filter_by(persons_id=id,resource_id=data['resources_id']).first()
    if resource_access:
        resource_access.is_active = data['is_active']
        db.session.commit()
        
        response_object = {
        'status': 'success',
        'message': 'Successfully updated persons resource access'
        }
        return response_object, 201
    else:
        return "Resource Access for this persons not found"
        

def get_person_by_email(data):
    email = data['email']
    return Persons.query.filter_by(email=email,was_validated=1).first()

def validate_persons_email(email):

    #Search for person in database and activate
    person = Persons.query.filter_by(email=email,was_validated=0).first()

    if person:
        person.was_validated = 1
        db.session.commit()
        return 'Person was validated'
    else:
        return 'Person not found so could not be validated'

def add_invite_to_resource(email,resource_id,from_date,to_date):

    #Search for person in database and activate
    person = Persons.query.filter_by(email=email,was_validated=1).first()

    spaced_from_date = from_date.replace('*',' ')
    spaced_to_date = to_date.replace('*',' ')

    if person:

        new_item = ResourceAccess(
            resource_id=resource_id,
            persons_id=person.id,
            roles_id=2,
            is_active=1,
            from_date = spaced_from_date,
            to_date= spaced_to_date,
            created_at = datetime.datetime.utcnow()
        )

        db.session.add(new_item)
        db.session.commit()
        return new_item.id
    else:
        return 'Person not found so could not be added to Resource'

def send_invitation(id,data):

    invite_person = Persons.query.filter_by(email=data['email'],was_validated=1).first()

    if invite_person:
      send_invitation_email(id,data)
      return "Invitation sent"
    else:
        return "Person not found in our database"

def send_validation_email(email):
    #To send by email the generated qr code image.
    fromaddr ="example@identikey.com"
    toaddr = "perahobuxi@idx4.com" # Se supone que aqui va el email de la persona que se registro
    msg = MIMEMultipart()
    msg['From'] = "example@identikey.com"
    msg['To'] = "perahobuxi@idx4.com"
    msg['Subject'] = "Identikey Validation"
    body = "Here is your validation link: http://ec2-52-21-122-184.compute-1.amazonaws.com:8888?/persons/validate?email={}".format(email)
    msg.attach(MIMEText(body, 'plain'))

    # img_data = open('/home/ubuntu/api-indentikey/app/uploads/{}.png'.format(randomId), 'rb').read()
    # ImgFileName = 'test.png'
    # image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    # msg.attach(image)
    # Here we create the actual mail server. It would be wise to create it for global use.
    server = smtplib.SMTP('smtp.mailgun.org', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(os.getenv("MAILGUN_USERNAME"),os.getenv("MAILGUN_PASSWORD")) # Need to put this credential in a .env or some other file
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print('Email sent')

def send_invitation_email(id,data):

    host_person = Persons.query.filter_by(id=id,was_validated=1).first()

    host_full_name = host_person.firstname +' '+ host_person.lastname

    resource = Resources.query.filter_by(id=data['resource_id']).first()

    escaped_from_date = data['from_date'].replace(' ','*')
    escaped_to_date = data['to_date'].replace(' ','*')

    #To send by email the generated qr code image.
    fromaddr ="example@identikey.com"
    toaddr = "perahobuxi@idx4.com" # Se supone que aqui va el email de la persona que se registro
    msg = MIMEMultipart()
    msg['From'] = "example@identikey.com"
    msg['To'] = "perahobuxi@idx4.com"
    msg['Subject'] = "{} has invited you".format(host_full_name)
    body = "{} has invited you to {} resource. Please click on the link to succesfully add you to {} resource: http://ec2-52-21-122-184.compute-1.amazonaws.com:8888/persons/invite/{}/resource?email={}&resource_id={}&from_date={}&to_date={}".format(host_full_name,resource.name,host_full_name,id,data['email'],data['resource_id'],escaped_from_date,escaped_to_date)
    msg.attach(MIMEText(body, 'plain'))

    # img_data = open('/home/ubuntu/api-indentikey/app/uploads/{}.png'.format(randomId), 'rb').read()
    # ImgFileName = 'test.png'
    # image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    # msg.attach(image)
    # Here we create the actual mail server. It would be wise to create it for global use.
    server = smtplib.SMTP('smtp.mailgun.org', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(os.getenv("MAILGUN_USERNAME"),os.getenv("MAILGUN_PASSWORD")) # Need to put this credential in a .env or some other file
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print('Email sent')

  

