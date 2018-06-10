from flask_jwt import current_identity
from flask_jwt import jwt_required
from flask_restful import Resource
from flask_restful import reqparse

class AccountPath(Resource):

	@jwt_required()
	def get(self):
		''' Returns URL to open for account'''
		return(AccountPath.url_from_user(current_identity))

	@staticmethod
	def url_from_user(user):

		'''Maps user to their account URL'''

		return 'www.google.com'
