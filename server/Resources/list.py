from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from server.authentication import SimpleAuthentication
from server.models import User, Bucket, ActivityLog, SharedEncryptionKey


class GetList(APIView):
    '''
    Returns a list of items in User's bashlist with their metadata
    '''

    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    def get(self, request, format='json'):

        email = request.META.get('HTTP_EMAIL')
        user = User.objects.get(email=email)

        try:
            buckets = Bucket.objects.filter(owner=user, deleted=False,available=True)
            shared_buckets = Bucket.objects.filter(available=True,deleted=False,shared_with=user)
            if len(buckets) == 0 and len(shared_buckets)==0:
                return Response({"Empty": "T"})
            return_arr = [bucket.json_representation() for bucket in buckets]
            for bucket in shared_buckets:
                return_arr.append(bucket.json_representation())
            return Response({"Data": return_arr, "Empty": "F"})
        except Exception as e:
            return Response({"Error": "Y"}, 399)
