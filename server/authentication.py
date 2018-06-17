from rest_framework import authentication
from rest_framework import exceptions

class SimpleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('Email')
        password = request.META.get('Password')
        if not username or not password:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        if user.check_password(string(password)):
        	return (user,None)
      
        exceptions.AuthenticationFailed('Incorrect Password')


    