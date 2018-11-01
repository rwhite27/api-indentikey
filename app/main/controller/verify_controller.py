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

        #Se supone que aqui hay que mandarle el settings del recurso y la data que se va a mandar.
        data = request.form
        files =  request.files
        settings = request.json
        return verify(settings=settings,data=data,files=files)