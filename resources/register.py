import bcrypt
from flask_jwt import current_identity
from flask_jwt import jwt_required
from flask_restful import Resource
from flask_restful import reqparse
from models.pubkeys import PubKeyModel
from models.objects import FileModel
from models.users import UserModel

class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('email',type=str,required=True,help='email is a required field')
	parser.add_argument('password',type=str,required=True,help='password is a required field')

	def post(self):
		
		parser = reqparse.RequestParser()
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_email(data['email']):
			return {'BLCODE':'X2ISD'}

		user = UserModel(data['email'],bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()))
		user.save_to_db()
		return {'BLCODE':'USD23'}

	

	############ FOR TESTING PURPOSES ONLY ##############

	@jwt_required()
	def get(self):

		# pub_key = PubKeyModel('dsdsdsd','harsh')
		# pub_key.save_to_db()
		print(current_identity.email)
		file = FileModel('adsadassas','harsh')
		file.save_to_db()
		return {'message':'works'}

	#####################################################
