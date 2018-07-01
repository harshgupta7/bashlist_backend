from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from server.authentication import SimpleAuthentication
from server.models import User,Bucket,ActivityLog,SharedEncryptionKey
from werkzeug import secure_filename
from server.s3 import generate_s3_push_url,get_directory_data,generate_get_url

class RequestPushBucketURL(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def post(self,request,format='json'):


		email = request.META.get('HTTP_EMAIL')
		size = int(request.data['Size'])
		size = abs(size)
		bucket_name = request.data['Name']
		user = User.objects.get(email=email)

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
			url = generate_s3_push_url(s3_bucket_key,size_limit=1000*size)#1000x to specify in bytes
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
			url = generate_s3_push_url(s3_bucket_key,size_limit=size*1000)#1000x to specify in bytes
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
			bucket = Bucket(owner=user,name=bucket_name,saved_as=secure_filename(bucket_name),size=size,available=False)
			s3_bucket_key = '{}__{}'.format(user.s3_bucket_key,secure_filename(bucket_name))
			bucket.save()
			if user.virtual_size_used + size > user.virtual_size_limit:
				return Response({'Error':'Y'},423)
			user.virtual_size_used+=size
			user.save()
			file_encryption_key = user.encrypted_bucket_encryption_key
			url = generate_s3_push_url(s3_object_key=s3_bucket_key,size_limit=size*1000)#1000x to specify in bytes
			return Response({'Error':'N','Exist':'N','Shared':'N','Key':file_encryption_key,'URL':url}) 
		except Exception as e:
			return Response({'Error':'Y'},399)



class PushBucketConfirmation(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def post(self,request,format='json'):
		email = request.META.get('HTTP_EMAIL')
		name = request.data.get('Name')
		user = User.objects.get(email=email)
		shared = request.data.get('Shared')
		try:
			description = request.data.get('BLDESC')
		except:
			pass
		if shared=='Y':
			bucket = bucket.objects.get(is_shared=True,shared_with=user,name=name,available=True,deleted=False)
		else:
			bucket= Bucket.objects.filter(owner=user,name=name,deleted=False).latest('created_at')
		s3_bucket_key = s3_bucket_key='{}__{}'.format(user.s3_bucket_key,bucket.saved_as)
		size = get_directory_data(s3_bucket_key)
		if not size:
			return Response({'Error':'Y'},399)
		bucket.size_on_s3 = size
		bucket.s3_bucket_key = s3_bucket_key
		bucket.available = True
		log = ActivityLog(user=user,bucket=bucket,action='Up')
		log.save()
		if description:
			bucket.description = description
		bucket.save()
		return Response({'Error':'N'},225)