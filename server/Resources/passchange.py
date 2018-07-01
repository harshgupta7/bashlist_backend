from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from server.authentication import SimpleAuthentication
from server.models import User,Bucket,ActivityLog,SharedEncryptionKey
from werkzeug import secure_filename
from server.s3 import generate_s3_push_url,get_directory_data,generate_get_url



class RequestEncCreds(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,format='json'):
		email = request.META.get('HTTP_EMAIL')
		user = User.objects.get(email=email)
		
		fileKey = user.encrypted_bucket_encryption_key
		privKey = user.encrypted_priv_key
		return Response({'fKey':fileKey,'pKey':privKey},398)
		

class NewCredsPoster(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def post(self,request,format='json'):
		email = request.META.get('HTTP_EMAIL')
		user = User.objects.get(email=email)
		try:
			new_password = request.data['Password']
			encrypted_file_key = request.data['EncFileKey']
			encrypted_priv_key = request.data['EncPrivKey']

			user.set_password(new_password)
			user.encrypted_bucket_encryption_key = encrypted_file_key
			user.encrypted_priv_key = encrypted_priv_key
			user.save()
			return Response({'msg':'Done'},398)
		except:
			return Response({'msg':'Error'},399) 

