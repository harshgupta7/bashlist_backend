import bcrypt
from flask_jwt import current_identity
from flask_jwt import jwt_required
from flask_restful import Resource
from flask_restful import reqparse
from models.files import FileModel
from models.users import UserModel

class UserRegister(Resource):

	'''Method to register a new user'''

	parser = reqparse.RequestParser()
	parser.add_argument('email',type=str,required=True,help='email is a required field')
	parser.add_argument('password',type=str,required=True,help='password is a required field')

	@jwt_required
	def post(self):
		
		if current_identity.email!='harsh':
			return
		
		parser = reqparse.RequestParser()
		data = UserRegister.parser.parse_args()


		if UserModel.find_by_email(data['email']):
			return {'BLCODE':'X2ISD'}

		user = UserModel(data['email'],bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()))
		user.save_to_db()
		return {'BLCODE':'USD23'}

