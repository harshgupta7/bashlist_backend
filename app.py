from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.register import UserRegister
from resources.account import AccountPath
import os
from security import authenticate,identity
from datetime import timedelta
from flask import jsonify



app = Flask(__name__)
api = Api(app)
app.secret_key = 'If President Obama knew about the so called Russia meddling, why didnt he do anything about it'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')


app.config['JWT_AUTH_URL_RULE'] = '/bashlistauth'
jwt = JWT(app, authenticate, identity)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=20)
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                        'access_token': access_token.decode('utf-8'),
                        'BLCODE': 'CTR23'
                   })

@jwt.jwt_error_handler
def customized_error_handler(error):

	if error.description=="Invalid credentials":
		val = 'XRQ23'
	elif error.description=="Signature has expired":
		val = 'INC23'
	else:
		val = 'MMR23'

	return jsonify({'BLCODE':val})


@app.before_first_request
def create_tables():
	db.create_all()

api.add_resource(UserRegister,'/register')
api.add_resource(AccountPath,'/account')

if __name__ == '__main__':

	from db import db 
	db.init_app(app)
	app.run(debug=True)