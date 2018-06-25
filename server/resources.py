from django.http import Http404
from rest_framework.views import APIView
from server.authentication import SimpleAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from server.models import User,Bucket,ActivityLog,SharedEncryptionKey
from server.s3 import generate_s3_pull_url,generate_s3_put_url
from werkzeug import secure_filename
from server.s3 import generate_s3_pull_url,generate_s3_put_url,get_directory_data

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
			if len(buckets)==0:
				return Response({"Empty":"T"})
			return_arr = [bucket.json_representation() for bucket in buckets]
			return Response({"Data":return_arr,"Empty":"F"})
		except Exception as e:
			print(e)
			return Response({"Error":"Y"},399)


class GetAccountURL(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,format='json'):

		email = request.META.get('HTTP_EMAIL')
		user = User.objects.get(email=email)
		url = user.generate_account_url()
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

		#case 1: bucket is owned by user
		try:
			bucket = Bucket.objects.get(name=bucket_name,owner=user,deleted=False,available=True)
			decryption_key = user.encrypted_file_encryption_key
			s3_bucket_key = '{}__{}'.format(user.id,bucket.saved_as)
			url = user.generate_s3_pull_url(s3_bucket_key)
			#TODO:put in celery
			log = ActivityLog(user=user,bucket=bucket,action='Do')
			log.save()
			# -------
			return Response({'shared':'False','url':url,'key':decryption_key})
		except Bucket.DoesNotExist:
			pass 

		#case 2: bucket is shared with user.
		try:
			bucket = Bucket.objects.get(is_shared=True,available=True,deleted=False,name=bucket_name,shared_with=user)
			owner = bucket.owner
			s3_bucket_key = '{}__{}'.format(owner.id,bucket.saved_as)
			url = user.generate_s3_pull_url(s3_bucket_key)
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



class RequestPushBucketURL(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def post(self,request,format='json'):

		# return Response({'m':'kk'})

		email = request.META.get('HTTP_EMAIL')
		print(request.data)
		# print(request.body)
		size = int(request.data['Size'])
		size = abs(size)
		bucket_name = request.data['Name']
		user = User.objects.get(email=email)
		# return Response({'sd':'sds'})

		# Case 1: Bucket is private, and is owned by user.
		try:
			bucket = Bucket.objects.get(name=bucket_name,owner=user,available=True,deleted=False,is_shared=False)
			if size+user.virtual_size_used-bucket.size>user.virtual_size_limit:
				return Response({'Error':'Y'},423)
			bucket.size = size
			bucket.save()
			user.virtual_size_used+=size
			user.save()
			file_encryption_key = user.encrypted_bucket_encryption_key
			s3_bucket_key = '{}__{}'.format(user.id,bucket.saved_as)
			url = generate_s3_put_url(s3_bucket_key,size_limit=size)
			return Response({'Error':'N','Exist':'Y','Shared':'N','Key':file_encryption_key,'URL':url})
		except Bucket.DoesNotExist:
			pass

		# Case 2: Bucket is shared and is shared with user.
		try:
			bucket = Bucket.objects.get(name=bucket_name,shared_with=user,is_shared=True,deleted=False,available=True)
			bucket_owner = bucket.owner 
			if bucket_owner.virtual_size_used - bucket.size + size > bucket_owner.virtual_size_limit:
				if bucket_owner==user:
					return Response({'Error':'Y'},423)
				else:
					return Response({'Error':'Y'},424)
			s3_bucket_key = '{}__{}'.format(bucket_owner.id,bucket.saved_as)
			url = generate_s3_put_url(s3_bucket_key,size_limit=size)
			bucket_owner.virtual_size_used+=size
			bucket_owner.save()
			try:
				key = SharedEncryptionKey.objects.get(bucket=bucket,key_owner=user)
			except:
				return Response({'Error':'Y'},399)
			keyval = key.enrypted_bucket_encryption_key
			priv_key = user.encrypted_priv_key
			return Response({'Error':'N','Shared':'Y','Exist':'Y','PrivKey':priv_key,'key':keyval})
		except Bucket.DoesNotExist:
			pass

		# Case 3: New Bucket
		try:
			# s3_bucket_key = '{}__{}'.format(user.id,bucket.saved_as)
			bucket = Bucket(owner=user,name=bucket_name,saved_as=secure_filename(bucket_name),size=size,available=False)
			s3_bucket_key = s3_bucket_key='{}__{}'.format(user.s3_bucket_key,secure_filename(bucket_name))
			bucket.save()
			if user.virtual_size_used + size > user.virtual_size_limit:
				return Response({'Error':'Y'},423)
			user.virtual_size_used+=size
			user.save()
			file_encryption_key = user.encrypted_bucket_encryption_key
			url = generate_s3_put_url(s3_bucket_key,size_limit=size)
			return Response({'Error':'N','Exist':'N','Shared':'N','Key':file_encryption_key,'URL':url}) 
		except Exception as e:
			print(e)
			return Response({'Error':'Y'},399)

class PushBucketConfirmation(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def post(self):
		email = request.META.get('HTTP_EMAIL')
		name = request.data.get('Name')
		shared = request.data.get('Shared')
		try:
			description = request.data.get('HTTP_BLDESC')
		except:
			pass
		if shared=='Y':
			bucket = bucket.objects.get(is_shared=True,shared_with=user,name=name,available=True,deleted=False)
		else:
			bucket = Bucket.objects.get(owner=user,name=name,deleted=False)

		size = get_directory_data(bucket.saved_as)
		if not size:
			return Response({'Error':'Y'},399)
		
		bucket.size_on_s3 = size
		bucket.s3_bucket_key = '{}__{}'.format(user.s3_bucket_key,bucket.saved_as)
		bucket.available = True
		log = ActivityLog(user=user,bucket=bucket,action='Up')
		log.save()
		if description:
			bucket.description = description
		bucket.save()
		return Response({'Error':'N'},225)

class ShareBucketRequest(APIView):
	pass 


class DeleteBucketRequest(APIView):
	pass

class TestAuth(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,format='json'):

		return Response({'Valid':'T'})











