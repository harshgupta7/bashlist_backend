from django.http import Http404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from server.models import User

class UserRegister(APIView):

	def post(self, request, format='json'):

		permission_classes = (AllowAny,)


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

