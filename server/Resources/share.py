from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from server.authentication import SimpleAuthentication
from server.models import User, Bucket, ActivityLog, SharedEncryptionKey



class ShareBucketRequest(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    def get(self, request, bucket_name, format='json'):

        email = request.META.get('HTTP_EMAIL')
        user = User.objects.get(email=email)

        # case 1: bucket is owned by user
        try:
            bucket = Bucket.objects.get(name=bucket_name, owner=user, deleted=False, available=True)
            decryption_key = user.encrypted_file_encryption_key
            s3_bucket_key = '{}__{}'.format(user.id, bucket.saved_as)
            return Response({'is_owner': 'T', 'exist': 'T'})
        except Bucket.DoesNotExist:
            pass

        # case 2: bucket is shared with user.
        try:
            bucket = Bucket.objects.get(is_shared=True, available=True, deleted=False, name=bucket_name,
                                        shared_with=user)
            owner = bucket.owner
            return Response({'shared': 'F', 'exist': 'T'})
        except Bucket.DoesNotExist:
            return Response({'exist': 'F'}, 667)
