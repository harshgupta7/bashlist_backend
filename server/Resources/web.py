# REST APIs for website

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from server.authentication import SimpleAuthentication


class GetList(APIView):
    '''
    Returns a list of items in User's bashlist with their metadata
    '''

    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    def get(self, request, token, format='json'):

        email = request.META.get('HTTP_EMAIL')
        user = User.objects.get(email=email)

        try:
            buckets = Bucket.objects.filter(owner=user, deleted=False)
            if len(buckets) == 0:
                return Response({"Empty": "T"})
            return_arr = [bucket.json_representation() for bucket in buckets]
            return Response({"Data": return_arr, "Empty": "F"})
        except Exception as e:
            print(e)
            return Response({"Error": "Y"}, 399)


class PostSupportTicket(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SimpleAuthentication,)

    pass
