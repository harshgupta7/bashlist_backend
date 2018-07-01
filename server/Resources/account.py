from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from server.authentication import SimpleAuthentication
from server.models import User, Bucket, ActivityLog, SharedEncryptionKey
from werkzeug import secure_filename
from server.s3 import generate_s3_push_url, get_directory_data, generate_get_url


class GetAccountURL(APIView):
    '''
    Return's user's UURL
    '''

    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    def get(self, request, format='json'):
        email = request.META.get('HTTP_EMAIL')
        user = User.objects.get(email=email)
        url = user.generate_account_url()
        return Response({'Url': url})
