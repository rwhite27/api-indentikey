from flask import request
from flask_restplus import Resource

from ..util.dto import RegisterDto
from ..service.register_service import register_qr_code, register_fingerprint, register_face, register_voice

api = RegisterDto.api


@api.route('/qr-code')
class PersonRegistration(Resource):
    @api.response(201,"Set qr code for person")
    @api.doc('Set qr code for person')
    def post(self):
        """et qr code for person """
        #Se supone que aqui hay que mandarle el settings del recurso y la data que se va a mandar.
        if request.files:
            data = request.form.copy()
            data.update(request.files)
        else:
            data = request.form
        
        # return str(data)
        settings = request.json
        return register_qr_code(data=data)

@api.route('/fingerprint')
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
        return register_fingerprint(data=data)


@api.route('/face')
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
        return register_face(data=data)

@api.route('/voice')
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
        return register_voice(data=data)