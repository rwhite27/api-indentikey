from flask import request
from flask_restplus import Resource

from ..util.dto import RegisterDto
from ..service.register_service import register_biometrics

api = RegisterDto.api


@api.route('/register')
class PersonRegistration(Resource):
    @api.response(201,"Verify person's identification")
    @api.doc('verify a person')
    def post(self):
        """Verify a person """

        #Se supone que aqui hay que mandarle el settings del recurso y la data que se va a mandar.
        if request.files:
            data = request.form.copy()
            data.update(request.files)
        else:
            data = request.form
        
        # return str(data)
        settings = request.json
        return register_biometrics(settings=settings,data=data)