from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from server.authentication import SimpleAuthentication
from server.models import User, Bucket, ActivityLog, SharedEncryptionKey
from server.s3 import generate_get_url


class RequestPullBucketURL(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    def get(self, request, bucket_name, format='json'):

        email = request.META.get('HTTP_EMAIL')
        user = User.objects.get(email=email)
        bucket_name = str(bucket_name)
        # case 1: bucket is owned by user
        try:
            bucket = Bucket.objects.get(name=bucket_name, owner=user, deleted=False, available=True)
            decryption_key = user.encrypted_bucket_encryption_key
            s3_bucket_key = '{}__{}'.format(user.id, bucket.saved_as)
            url = generate_get_url(s3_bucket_key)
            # TODO:put in celery
            log = ActivityLog(user=user, bucket=bucket, action='Do')
            log.save()
            # -------
            return Response({'shared': 'False', 'url': url, 'key': decryption_key}, 285)
        except Bucket.DoesNotExist:
            pass

        # case 2: bucket is shared with user.
        try:
            bucket = Bucket.objects.get(is_shared=True, available=True, deleted=False, name=bucket_name,
                                        shared_with=user)
            owner = bucket.owner
            s3_bucket_key = '{}__{}'.format(owner.id, bucket.saved_as)
            url = user.generate_s3_pull_url(s3_bucket_key)
            encryption_key = SharedEncryptionKey.objects.filter(key_owner=user, bucket=bucket)
            encrypted_priv_key = user.encrypted_priv_key
            # TODO:put in celery
            log = ActivityLog(user=user, bucket=bucket, action='Do')
            log.save()
            # ----
            return Response({'url': url, 'key': encryption_key,
                             'unlock_key': encryption_priv_key, 'shared': 'True', 'Error_message': 'None'}, 285)
        except Bucket.DoesNotExist:
            return Response({'Error_message': "No Buckets Found"}, 284)
