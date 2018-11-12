from flask import request
from flask_restplus import Resource

from ..util.dto import VerifyDto
from ..service.verify_service import verify_qr_code,verify_fingerprint,verify_face,verify_voice
from app.main.model.resources import Resources
from app.main.model.resource_settings import ResourceSettings
from app.main.model.verification_methods import VerificationMethods
from app.main.model.resource_access import ResourceAccess

api = VerifyDto.api


@api.route('/')
class PersonVerification(Resource):
    @api.response(201,"Verify person's identification")
    @api.doc('verify a person')
    def post(self):
        """Verify a person """

        #Podemos hacer el switch aqui en vez de en los servicios
        if request.files:
            data = request.form.copy()
            data.update(request.files)
        else:
            data = request.form

        # #Search for resource object and then resource setting
        # resource = Resources.query.filter_by(code=data['code']).first()

        # if resource:
        #     allowed = is_person_allowed(resource.id,data['persons_id'])
        #     if allowed:
        #         resource_settings = ResourceSettings.query.filter_by(resources_id=resource.id).all()
        #         if resource_settings:
        #             for resource_setting in resource_settings:

        #                 #Search for verification method name
        #                 verification_method = VerificationMethods.query.filter_by(id=resource_setting.verification_methods_id).first()

        #                 if verification_method:
        #                     #Send to verification method function                    
        #                     option = verification_method.name

        #                     if option == 'QR_CODE':
        #                        return  verify_qr_code(data=data)
        #                     elif option == 'FINGERPRINT':
        #                        return  verify_fingerprint(data=data)
        #                     elif option == 'FACERECOG':
        #                        return  verify_face(data=data)
        #                     elif option == 'VOICERECOG':
        #                        return verify_voice(data=data)
        #                     else:
        #                         return 'Invalid verification'
        #                 else:
        #                     return 'No verification method found'
        #     else:
        #         return "Person not allowed"
        # else:
        #     return 'Resource not found'
        # #Need to make a for in statement so that the verification passes through every function depending on settings

        # return 'hello'
        option = 'FACERECOG'

        if option == 'QR_CODE':
           return  verify_qr_code(data=data)
        elif option == 'FINGERPRINT':
           return  verify_fingerprint(data=data)
        elif option == 'FACERECOG':
           return  verify_face(data=data)
        elif option == 'VOICERECOG':
           return verify_voice(data=data)
        else:
            return 'Invalid verification'

def is_person_allowed(resources_id,persons_id):

        resource_access = ResourceAccess.query.filter_by(resource_id=resources_id,persons_id=persons_id,is_active=1).first()

        if resource_access:
            return True
        else:
            return False

        