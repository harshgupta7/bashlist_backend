from flask_restful import Resource,reqparse
from flask_jwt import jwt_required,current_identity

class AccountPath(Resource):

	@jwt_required()
	def get(self):

		return(AccountPath.url_from_user(current_identity))

	@staticmethod
	def url_from_user(user):
		return 'www.google.com'
