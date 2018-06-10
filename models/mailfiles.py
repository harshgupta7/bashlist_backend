import uuid
from db import db
import random

class MailShares(db.Model):

	__tablename__ = 'mailedfiles'

	id = db.Column(db.Text,primary_key=True)
	created_at = db.Column(db.DateTime,server_default=db.func.now())
	updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
	owner_id = db.Column(db.Text,nullable=False)
	file_id = db.Column(db.Text,nullable=False)
	receipient_id = db.Column(db.Text,nullable=False)
	file_url = db.Column(db.Text,nullable=False)
	sent = db.Column(db.Boolean,default=False)
	downloaded = db.Column(db.Boolean,default=False)

	def __init__(self,owner_id,receipient_id,file_id,file_url):

		self.id = str(uuid.uuid3(uuid.NAMESPACE_DNS, '{}{}{}'.format(owner_id,str(random.random()),str(db.func.now()))))
		self.owner_id = owner_id
		self.file_url = file_url
		self.file_id = file_id
		self.receipient_id = receipient_id
		self.file_id = file_id

	def save_to_db(self):

		db.session.add(self)
		db.session.commit()

	@staticmethod
	def find_by_id(_id):
		MailShares.query.filter_by(id=_id).first()




