import uuid
from django.db import models

class User(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	email = models.EmailField(max_length=255,blank=False,unique=True,null=False)
	password = models.CharField(max_length=255,null=False,blank=False)
	verified = models.BooleanField(default=False,blank=False)
	size_used = models.IntegerField(default=0, blank=False,null=False)
	size_limit = models.IntegerField(default=500000, blank=False,null=False)
	s3_bucket = models.CharField(max_length=255,default='central')
	s3_bucket_key = models.CharField(max_length=255,null=False,unique=True)


class Bucket(models.Model):

	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	owner_id = models.ForeignKey(User,on_delete=models.CASCADE)

