from rest_framework import authentication
from rest_framework import exceptions
from server.models import User

class SimpleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_EMAIL')
        password = request.META.get('HTTP_PASSWORD')
        if not username or not password:
            return None
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        if user.check_password(str(password)):
        	return (user,None)
      
        exceptions.AuthenticationFailed('Incorrect Password')


    