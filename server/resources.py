from django.http import Http404
from rest_framework.views import APIView
from server.authentication import SimpleAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from server.models import User,Bucket

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


class PullBucket(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,bucket_name,format='json'):

		email = request.META.get('HTTP_EMAIL')
		user = User.objects.get(email=email)

		try:
			bucket = Bucket.objects.get(name=bucket_name,owner=user,deleted=False)
		except:
			return Response({"Error_message":"No Buckets Found"},667)

		decryption_key = user.encrypted_file_encryption_key

		url = user.generate_s3_pull_url(user,bucket.saved_as)
		return Response({'URL':url,'Key':key})




















