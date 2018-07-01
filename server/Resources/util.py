from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from server.authentication import SimpleAuthentication
from server.models import User, Bucket, ActivityLog, SharedEncryptionKey


class UserRegister(APIView):
    '''
    Public API for User Registration
    '''

    permission_classes = (AllowAny,)

    def post(self, request, format='json'):

        email = request.data['Email']
        password = request.data['Password']
        if email is None or password is None:
            return Response({'message': 'Email and Password are required fields'})
        try:
            user = User.objects.get(email=email)
            if user:
                return Response({'message': 'Email alreaxy exists'})
        except:
            pass

        try:
            User.objects.create_user(email=email, password=password)
            return Response({'message': 'User created successfully'})
        except Exception as e:
            return Response({'message': '{}'.format(e)})


class TestAuth(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    def get(self, request, format='json'):
        return Response({'Valid': 'T'})


class GetPublicKey(APIView):
    # TODO: make multi-user compatible
    '''
    Returns Public Key of a User
    '''

    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    def get(self, request, other_user, format='json'):
        try:
            other = User.objects.get(email=other_user, deleted=False)
        except User.DoesNotExist:
            return Response({'Error_message': 'User Does Not Exist'}, 889)
        return Response({'pubkey': other.pub_key})
