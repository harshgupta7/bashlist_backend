import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from server.authentication import SimpleAuthentication
from server.models import Bucket, User
from server.s3 import delete_object


class GetBucketInfo(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    def get(self, request, dir_name, format='json'):

        email = request.META.get('HTTP_EMAIL')
        user = User.objects.get(email=email)

        # Buckets where user is owner
        try:
            bucket = Bucket.objects.get(name=dir_name, owner=user, deleted=False, available=True)
            if bucket.is_shared:
                return Response({'shared': 'True', 'owner': 'True', 'exist': 'True'}, 200)
            else:
                return Response({'shared': 'False', 'owner': 'True', 'exist': 'True'}, 200)

        except Bucket.DoesNotExist:
            pass

        # Bucket where user is not owner but is shared with him
        try:
            Bucket.objects.get(name=dir_name, is_shared=True, available=True, deleted=False, shared_with=user)
            return Response({'shared': 'True', 'owner': 'False', 'exist': 'True'}, 200)
        except Bucket.DoesNotExist:
            return Response({'shared': 'False', 'owner': 'False', 'exist': 'False'}, 367)


class DeleteBucketConf(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    def get(self, request, random_waste, dir_name, shared, owner, format='json'):

        email = request.META.get('HTTP_EMAIL')
        user = User.objects.get(email=email)

        is_shared = shared == 'True'
        is_owner = owner == 'True'

        if is_owner:

            bucket = Bucket.objects.get(name=dir_name, owner=user, is_shared=is_shared, deleted=False, available=True)
            bucket_size = bucket.size
            s3_size = bucket.size_on_s3
            user.virtual_size_used = user.virtual_size_used - bucket_size
            user.real_size_used = user.real_size_used - s3_size
            user.save()
            delete_object(bucket.s3_bucket_key)
            bucket.deleted = True
            bucket.deleted_at = datetime.datetime.now()
            bucket.s3_bucket_key = None
            if is_shared:
                bucket.is_shared = False
                bucket.shared_with.clear()
            bucket.save()

        else:
            bucket = Bucket.objects.get(name=dir_name, is_shared=is_shared, deleted=False, available=True,
                                        shared_with=user)
            bucket.shared_with.remove(user)
            count = bucket.shared_with.distinct().all()
            if count == 0:
                bucket.is_shared = False
                bucket.shared_with.clear()
            bucket.save()

        return Response({'done': 'True'}, 200)
