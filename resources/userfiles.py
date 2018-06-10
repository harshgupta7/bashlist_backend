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

		return current_identity.list_all_files()




class FileUpload(Resource):

	
	@jwt_required()
	def post(self):
		description = str(request.headers.get('Description'))
		file = request.files['file']
		filename = file.filename

		saved_as = secure_filename(filename)
		path = '{}/{}'.format(current_identity.location,saved_as)
		file.save(path)
		size = os.path.getsize(path)


		if current_identity.size_used + size > current_identity.size_limit:
			return {'BLCODE':'OVX23'}

		if filename not in current_identity.get_all_file_names()['files']:
			record =  FileModel(filename,saved_as,current_identity.id,description,size) 
			record.save_to_db()
			user = current_identity
			user.size_used = user.size_used + size 
			user.save_to_db()
			return {'BLCODE':"LMV23"}
		else:
			record = FileModel.find_by_owner_name(current_identity.id,filename)
			record.size = size
			record.description = description
			record.save_to_db()
			return {'BLCODE':"LMV23"}


class FileGet(Resource):
	@jwt_required()
	def get(self,name):

		if name not in current_identity.get_all_file_names()['files']:
			return {'BLCODE':'NE235'}
		else:
			loc = current_identity.location
			file = FileModel.find_by_owner_name(current_identity.id,name)
			path = '{}/{}'.format(loc,file.saved_as)
			return send_file(path,as_attachment=False,attachment_filename=name)

	@jwt_required()
	def delete(self,name):
		pass 


class TestUpload(Resource):
	def post(self):
		file = request.files['file']
		filename = file.filename
		saved_as = secure_filename(filename)
		path = UserModel.find_by_email("harsh").location
		file.save('{}/{}'.format(path,saved_as))
		return {'BLCODE':"SUCCESS"}


