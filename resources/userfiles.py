from flask_jwt import current_identity
from flask_jwt import jwt_required
from flask_restful import Resource
from flask import request
from flask_restful import reqparse
from models.users import UserModel
from models.files import FileModel
from werkzeug import secure_filename
import os
from flask import send_file


class ListFiles(Resource):

	@jwt_required()
	def get(self):

		'''Method to return array representation of all files of user making request'''

		user = UserModel.find_by_email(current_identity.email)
		if not user:
			return {'BLCODE':'XEF23'}

		return user.list_all_files()




class File(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('description', type=str, required=False)

	@jwt_required()
	def post(self,name):

		parser = reqparse.RequestParser()
		data = File.parser.parse_args()
		if 'description' in data.keys():
			desc = data['description']
		else:
			desc = ''

		file = request.files['file']
		filename = file.filename
		saved_as = secure_filename(filename)
		path = '{}/{}'.format(current_identity.location,saved_as)
		file.save(path)
		size = os.path.getsize(path)

		record =  FileModel(filename,saved_as,current_identity.id,desc,size) 
		record.save_to_db()
		return "SUCCESS"

	@jwt_required()
	def get(self,name):
		
		if name not in current_identity.get_all_file_names()['files']:
			return "FAILURE"
		else:
			loc = current_identity.location
			file = FileModel.find_by_owner_name(current_identity.id,name)
			path = '{}/{}'.format(loc,file.saved_as)
			send_file(path,as_attachment=False,attachment_filename=name)
			return "PASS"

	@jwt_required()
	def delete(self,name):
		pass 

