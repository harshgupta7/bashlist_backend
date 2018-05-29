from models.users import UserModel
import bcrypt

def authenticate(email, password):

	user = UserModel.find_by_email(email)
	if not user:
		return None
	if bcrypt.checkpw(password.encode('utf-8'), user.password):
		return user 

def identity(payload):

	user_id = payload['identity']
	return UserModel.find_by_id(user_id)

