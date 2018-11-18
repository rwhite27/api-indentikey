from flask import request
from flask_restplus import Resource

from ..util.dto import VerifyDto
from ..service.verify_service import verify_qr_code,verify_fingerprint,verify_face,verify_voice
from app.main.model.resources import Resources
from app.main.model.resource_settings import ResourceSettings
from app.main.model.verification_methods import VerificationMethods
from app.main.model.resource_access import ResourceAccess
import json

api = VerifyDto.api


@api.route('/')
class PersonVerification(Resource):
    @api.response(201,"Verify person's identification")
    @api.doc('verify a person')
    def post(self):
        """Verify a person """


        verification_result = False
        results = {}
        resource_thresholds = {}

        #Podemos hacer el switch aqui en vez de en los servicios
        if request.files:
            data = request.form.copy()
            data.update(request.files)
        else:
            data = request.form

        qr_results = verify_qr_code(data=data)

        # #Search for resource object and then resource setting
        resource = Resources.query.filter_by(code=data['code']).first()

        if resource:
            allowed = is_person_allowed(resource.id,qr_results)
            if allowed:
                resource_settings = ResourceSettings.query.filter_by(resources_id=resource.id,is_deleted=0).all()
                if resource_settings:
                    for resource_setting in resource_settings:

                        #Search for verification method name
                        verification_method = VerificationMethods.query.filter_by(id=resource_setting.verification_methods_id).first()

                        if verification_method:
                            #Send to verification method function                    
                            option = verification_method.name
                            if option == 'FINGERPRINT':
                                finger_results = json.loads(verify_fingerprint(data=data))
                                if finger_results['verification']:
                                    confirm_id = finger_results['verification'].replace('(','').replace(')','').split(',')[0].replace("'",'')
                                    if int(confirm_id) == qr_results:
                                        verification_result = True
                                    else:
                                        verification_result = False
                                else:
                                    verification_result = False
                            elif option == 'FACERECOG':
                                face_results = json.loads(verify_face(data=data))
                                if face_results['verification']:
                                    verification_result = True
                                else:
                                    verification_result = False
                            elif option == 'VOICERECOG':
                               verification_result = verify_voice(data=data,id=qr_results)
                            else:
                                return 'Invalid verification'
                            
                            results[verification_method.name] = verification_result
                            resource_thresholds[verification_method.name]= resource_setting.threshold
                        else:
                            return 'No verification method found'
                    return confirm_identity(minimun_threshold=resource.min_threshold,results=results,resource_thresholds=resource_thresholds)
            else:
                return "Person not allowed"
        else:
            return 'Resource not found'

def is_person_allowed(resources_id,persons_id):

        resource_access = ResourceAccess.query.filter_by(resource_id=resources_id,persons_id=persons_id,is_active=1).first()

        if resource_access:
            return True
        else:
            return False

def confirm_identity(minimun_threshold,results,resource_thresholds):

    confirmation_total = 0
    for (key,value) in results.items():
        if value == True:
            confirmation_total += resource_thresholds[key]
    return results
    if confirmation_total >= minimun_threshold:
        return True
    else:
        return False

