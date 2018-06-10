import uuid
import os
import random
import sendgrid
from flask import send_file
from flask_jwt import current_identity
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt import jwt_required 
from models.mailfiles import MailShares
from models.files import FileModel
from models.users import UserModel
from url import URL
from sendgrid.helpers.mail import Content,Email,Mail



sg = sendgrid.SendGridAPIClient(apikey='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')



class SendMailWithFile(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('Recs', type=str, required=True, help='receipients is a required field')
	parser.add_argument('Filename',type=str,required=True,help='filename is a required field')


	@jwt_required()
	def post(self):

		parser = reqparse.RequestParser()
		data = SendMailWithFile.parser.parse_args()

		file = FileModel.find_by_owner_name(current_identity.id,data['Filename'])
		if not file:
			return {'BLCODE':'FME98'}
		recstring = data['Recs']
		receipients = [x for x in recstring.split(';;;')]
		receivers = []

		url = '{}/filedownloader/{}/{}/{}'.format(URL,uuid.uuid4().hex,file.id,uuid.uuid4().hex)

		for x in receipients:


			user = UserModel.find_by_email(x)
			if user:
				f = MailShares(owner_id=current_identity.id,receipient_id=user.id,file_id=file.id,file_url=url)
				f.save_to_db()
			else:
				receiv = "OUTSIDE"
				f = MailShares(owner_id=current_identity.id,receipient_id=receiv,file_id=file.id,file_url=url)
				f.save_to_db()


			try:
				from_email = Email('harshgupta.src@gmail.com')
				to_email = Email(x)
				subject = "Bashlist - {} shared {} with you.\
				\
				\
				--\
				Bashlist Team".format(str(current_identity.email).title(),str(file.name).title())
				content = Content("text/plain", "Download Link: {}".format(url))
				mail = Mail(from_email, subject, to_email, content)
				response = sg.client.mail.send.post(request_body=mail.get())
			except:
				pass

		return {'BLCODE':'MLSC2'}



class DownloadMailedFile(Resource):

	def get(self,one,realval,three):

		file = FileModel.find_by_id(realval)
		loc = file.find_location()
		if loc:
			return send_file(loc,as_attachment=True,attachment_filename=file.name)
		else:
			render_template('404.html')


