from .models import Bucket
from rest_framework.views import APIView

class BucketList(APIView):

	def get(self,request,format=None):
		buckets = Bucket.objects.query.all(owner_id=)

