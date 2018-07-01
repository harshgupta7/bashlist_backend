from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from server.authentication import SimpleAuthentication

class GetBucketInfo(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,dir_name,format='json'):

		email = request.META.get('HTTP_EMAIL')
		user = User.objects.get(email=email)

		#Buckets where user is owner
		try:
			bucket = Bucket.objects.get(name=dir_name,owner=user,deleted=False,available=True)
			if bucket.is_shared:
				return Response({'shared':'True','owner':'True','exist':'True'})
			else:
				return Response({'shared':'True','owner':'True','exist':'True'})

		except Bucket.DoesNotExist:
			pass 

		# Bucket where user is not owner but is shared with him
		try:
			bucket = Bucket.objects.get(name=dir_name,is_shared=True,available=True,deleted=False,shared_with=user)
			return Response({'shared':'True','owner':'False','exist':'True'})
		except:
			return Response({'shared':'False','owner':'False','exist':'False'})


class DeleteBucketConf(APIView):

	permission_classes = (IsAuthenticated,)
	authentication_classes = (SimpleAuthentication,)

	def get(self,request,random_waste,dir_name,shared,owner,format='json'):

		email = request.META.get('HTTP_EMAIL')
		user = User.objects.get(email=email)

		is_shared = shared=='True'
		owner = owner=='True'

		