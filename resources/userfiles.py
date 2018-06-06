from flask_jwt import current_identity
from flask_jwt import jwt_required
from flask_restful import Resource
from flask_restful import reqparse
from models.users import UserModel


class ListFiles(Resource):

	@jwt_required()
	def get(self):

		'''Method to return array representation of all files of user making request'''

		user = UserModel.find_by_email(current_identity.email)
		if not user:
			return {'BLCODE':'XEF23'}

		return user.list_all_files()




class SyncUp(Resource):

	@jwt_required
	