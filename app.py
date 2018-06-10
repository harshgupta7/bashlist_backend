import os
from datetime import timedelta
import random
from flask import Flask
from flask import jsonify
from flask import render_template
from flask_jwt import JWT
from flask_restful import Api
from resources.register import UserRegister
from resources.account import AccountPath
from resources.mailer import SendMailWithFile,DownloadMailedFile
from resources.userfiles import ListFiles,FileUpload,FileGet,TestUpload
from security import authenticate,identity


app = Flask(__name__)
api = Api(app)



app.secret_key = 'If President Obama knew about the so called \
Russia meddling, why didnt he do anything about it'

#ORM Configs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',\
	'sqlite:///data.db')

# JWT Configs
app.config['JWT_AUTH_URL_RULE'] = '/bashlistauth'
jwt = JWT(app, authenticate, identity)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=6)
app.config['JWT_AUTH_USERNAME_KEY'] = 'Email'
app.config['JWT_AUTH_PASSWORD_KEY'] = 'Password'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

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

# #Only for dev server
# @app.before_first_request
# def create_tables():
# 	db.create_all()




### ENDPOINTS ______________________________

api.add_resource(UserRegister,'/register')
api.add_resource(AccountPath,'/account')
api.add_resource(ListFiles,'/getallfiles')
api.add_resource(FileUpload,'/filesync')
api.add_resource(FileGet,'/filedown/<string:name>')
api.add_resource(SendMailWithFile,'/sendmail')
api.add_resource(DownloadMailedFile,'/filedownloader/<string:one>/<string:realval>/<string:three>')
# api.add_resource(FileMailer,'/sendmail1')





if __name__ == '__main__':

	from db import db 
	db.init_app(app)
	#Only for dev server
	@app.before_first_request
	def create_tables():
		db.create_all()
	app.run(debug=True,use_reloader=False)