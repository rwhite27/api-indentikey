from flask import request
from flask_restplus import Resource

from ..util.dto import VerifyDto
from ..service.verify_service import verify_qr_code,verify_fingerprint,verify_face,verify_voice

api = VerifyDto.api


@api.route('/verify')
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

        #Need to make a for in statement so that the verification passes through every function depending on settings
        option = 'VOICERECOG'

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
        