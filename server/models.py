import uuid
from Crypto.PublicKey import RSA
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.s3_bucket_key = user.id
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.s3_bucket_key = user.id
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	email = models.EmailField(max_length=255,blank=False,unique=True,null=False)
	verified = models.BooleanField(default=False,blank=False)
	encrypted_pub_key = models.TextField(max_length=2048,blank=False,unique=True,null=True)
	encrypted_priv_key = models.TextField(max_length=2048,blank=False,unique=True,null=True)
	size_used = models.IntegerField(default=0)
	size_limit = models.IntegerField(default=500000, blank=False,null=False)
	s3_bucket = models.CharField(max_length=255,default='central')
	s3_bucket_key = models.CharField(max_length=255,null=False,unique=True)
	objects = UserManager()

	USERNAME_FIELD = 'email'

	

	
  

class Bucket(models.Model):

	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	owner = models.ForeignKey('User',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	encrypted_with = models.ForeignKey('IndividualEncryptionKey',null=True,on_delete=models.SET_NULL)
	name = models.CharField(max_length=255,null=False,blank=False)
	saved_as = models.CharField(max_length=255,null=False,blank=False)
	size = models.IntegerField(blank=False,null=False,default=0)
	description = models.TextField(max_length=500,null=True)
	s3_bucket = models.CharField(max_length=255,default='central')
	s3_bucket_key = models.CharField(max_length=255,null=False,unique=True)
	deleted = models.BooleanField(default=False)
	deleted_at = models.DateTimeField(null=True)



class EmailBucket(models.Model):

	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	download_url = models.URLField(null=False)
	sender = models.ForeignKey(User,null=False,editable=False,on_delete=models.CASCADE)
	bucket = models.ForeignKey(Bucket,null=False,editable=False,on_delete=models.CASCADE)
	receiver = models.EmailField(max_length=255,blank=False,null=False,editable=False)
	bucket_exists = models.BooleanField(default=True)
	downloaded = models.BooleanField(default=False)
	downloaded_at = models.DateTimeField(null=True)



class ShareBucket(models.Model):

	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	download_token = models.CharField(max_length=255,null=False,editable=False)
	sender = models.ForeignKey(User,null=False,editable=False,on_delete=models.CASCADE)
	bucket = models.ForeignKey(Bucket,null=False,editable=False,on_delete=models.CASCADE)
	receiver = models.EmailField(max_length=255,blank=False,null=False,editable=False)
	bucket_exists = models.BooleanField(default=True)
	encrypted = models.BooleanField(default=False)
	encrypted_with = models.ForeignKey('SharedEncryptionKey',null=True,on_delete=models.SET_NULL)
	downloaded = models.BooleanField(default=False)
	downloaded_at = models.DateTimeField(null=True)



class ActivityLog(models.Model):

	ACTIVITY_TYPES = (
        ('Do', 'Downloaded'),
        ('Up', 'Uploaded'),
        ('De', 'Deleted'),
        ('Sh','Shared'),
        ('Em', 'Emailed')
    )
	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User,null=False,editable=False,on_delete=models.CASCADE)
	bucket = models.ForeignKey(Bucket,null=False,editable=False,on_delete=models.CASCADE)
	action = models.CharField(max_length=2, choices=ACTIVITY_TYPES)

class IndividualEncryptionKey(models.Model):
	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	encrypted_key = models.TextField(null=False)
	owner = models.ForeignKey(User,on_delete=models.CASCADE)


class SharedEncryptionKey(models.Model):
	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	encrypted_key = models.TextField(null=False)
	created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='sender')
	created_for = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='receiver')	






	

