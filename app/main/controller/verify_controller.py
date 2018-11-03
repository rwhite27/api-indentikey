from flask import request
from flask_restplus import Resource

from ..util.dto import VerifyDto
from ..service.verify_service import verify

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
        settings = request.json
        return verify(settings=settings,data=data)