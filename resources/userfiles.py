from flask_restful import Resource,reqparse
from models.users import UserModel


class ListFiles(Resource):

	# parser = reqparse.RequestParser()
	# parser.add_argument('filename',type=str,required=True,help='filename is a required field')
	# parser.add_argument('password',type=str,required=True,help='password is a required field')

	def get(self,email):

		user = UserModel.find_by_email(email)
		if not user:
			return {'BLCODE':'XEF23'}

		return user.list_all_files()

	# def post(self,email):



