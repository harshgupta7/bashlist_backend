from django.http import Http404
from rest_framework.views import APIView
from server.authentication import SimpleAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from server.models import User,Bucket,ActivityLog,SharedEncryptionKey
from server.s3 import generate_s3_pull_url,generate_s3_push_url
from werkzeug import secure_filename

class UserRegister(APIView):

	permission_classes = (AllowAny,)

	def post(self, request, format='json'):

		email = request.data['Email']
		password = request.data['Password']
		if email is None or password is None:
			return Response({'message':'Email and Password are required fields'})
		try:
			user = User.objects.get(email=email)
			if user:
				return Response({'message':'Email already exists'})
		except:
			pass

		try:
			User.objects.create_user(email=email,password=password)
			return Response({'message':'User created successfully'})
		except Exception as e:
			return Response({'message':'{}'.format(e)})

class GetList(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,format='json'):

		email = request.META.get('HTTP_EMAIL')
		user = User.objects.get(email=email)
		
		try:
			buckets = Bucket.objects.filter(owner=user,deleted=False)
			return_arr = [bucket.json_representation() for bucket in buckets]
			return Response({"Data":return_arr},200)
		except:
			return Response({"Error_message":"No Buckets Found"})


class GetAccountURL(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,format='json'):

		email = request.META.get('HTTP_EMAIL')
		user = User.objects.get(email=email)
		url = user.get_account_url()
		return Response({'Url':url})


class GetPublicKey(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,other_user,format='json'):
		try:
			other = User.objects.get(email=other_user,deleted=False)
		except User.DoesNotExist:
			return Response({'Error_message':'User Does Not Exist'},889)
		return Response({'pubkey':other.pub_key})


class RequestPullBucketURL(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,bucket_name,format='json'):

		email = request.META.get('HTTP_EMAIL')
		user = User.objects.get(email=email)

		try:
			bucket = Bucket.objects.get(name=bucket_name,owner=user,deleted=False,available=True)
			decryption_key = user.encrypted_file_encryption_key
			url = user.generate_s3_pull_url(bucket)
			#TODO:put in celery
			log = ActivityLog(user=user,bucket=bucket,action='Do')
			log.save()
			# -------
			return Response({'shared':'False','url':url,'key':decryption_key})
		except Bucket.DoesNotExist:
			pass 

		try:
			bucket = Bucket.objects.get(is_shared=True,available=True,deleted=False,name=bucket_name,shared_with=user)
			url = user.generate_s3_pull_url(bucket)
			encryption_key = SharedEncryptionKey.objects.filter(key_owner=user,bucket=bucket)
			encrypted_priv_key = user.encrypted_priv_key
			#TODO:put in celery
			log = ActivityLog(user=user,bucket=bucket,action='Do')
			log.save()
			# ----
			return Response({'url':url,'key':encryption_key,
					'unlock_key':encryption_priv_key,'shared':'True','Error_message':'None'})
		except Bucket.DoesNotExist:
			return Response({'Error_message':"No Buckets Found"},667)			


# class RequestPushBucketURL(APIView):
	

# 	permission_classes = (IsAuthenticated,)
# 	authentication_classes = (SimpleAuthentication,)

# 	def post(self,request,bucket_name,size,format='json'):

# 		email = request.META.get('HTTP_EMAIL')
# 		size = request.data['Size']
# 		size = abs(size)
# 		bucket_name = request.data['Name']
# 		description = request.data['Description']
# 		user = User.objects.get(email=email)

# 		try:
# 			bucket = Bucket.objects.get(is_shared=True,available=True,deleted=False,name=bucket_name,shared_with=user)
			

# 		bucket = Bucket.objects.filter(name=bucket_name,owner=user,deleted=False)
# 		if len(bucket)==1:
# 			if (size-bucket.size+user.virtual_size_used>user.virtual_size_limit):
# 				return Response({'Error_message':'Insufficient Space'},423)
# 			else:
# 				bucket.size = size
# 				bucket.description = description
# 				bucket.save()
# 				url = generate_s3_push_url(user,bucket.saved_as,size)
# 				encryption_key = user.encrypted_bucket_encryption_key
# 				return Response({'url':url,'key':encryption_key,'shared':'F'})
# 		else:

# 			url,s3_key = generate_s3_push_url(user,secure_filename(bucket_name),size)
# 			encryption_key = user.encrypted_bucket_encryption_key
# 			bucket = Bucket(name=bucket_name,saved_as=secure_filename(bucket_name),available=False,s3_bucket_key=s3_key,description=description)
# 			bucket.save()
# 			return Response({'url':url,'shared':'F','key':encryption_key})




			
# 		else:



# 		try:
# 			bucket = Bucket.objects.get(name=bucket_name,owner=user,deleted=False)
# 			bucket.size = size 
# 			bucket.save()
# 			url = generate_s3_push_url(user,bucket,size)
# 			if bucket.is_shared:



# 		if user.virtual_size_used + size > user.virtual_size_limit:
# 			return Response({'Error_message':'Insufficient Space'},423)

# 		try:
# 			bucket = Bucket.objects.get(name=bucket_name,owner=user,deleted=False)
# 			bucket.size = size 

# 		except:
# 			pass

# 		decryption_key = user.encrypted_file_encryption_key
		
# 		#####TODO: put this in celery######
# 		log = ActivityLog(user=user,bucket=bucket,action='Do')
# 		log.save()
# 		###################################
		
# 		url = generate_s3_pull_url(user,bucket)
# 		return Response({'URL':url,'Key':key})





class ShareBucketRequest(APIView):
	pass 



class TestAuth(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,format='json'):

		return Response({'Valid':'T'})











