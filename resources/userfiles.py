from flask_restful import Resource,reqparse
from models.users import UserModel
from flask_jwt import jwt_required,current_identity


class ListFiles(Resource):

	@jwt_required()
	def get(self):

		'''Method to return array representation of all files of user making request'''

		user = UserModel.find_by_email(current_identity.email)
		if not user:
			return {'BLCODE':'XEF23'}

		return user.list_all_files()




