import uuid
from Crypto.PublicKey import RSA
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
from rest_framework.authtoken.models import Token
from server.utils import user_util_generate_file_encryption_key
from server.utils import user_util_generate_encrypted_key_pair
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given email and password.
        """
        if not email or not password:
            raise ValueError('Users must have an email address & password')

        user = self.model(
            email=self.normalize_email(email),
        )
        pub_key,priv_key = user_util_generate_encrypted_key_pair(password)
        file_encryption_key = user_util_generate_file_encryption_key(password)
        user.encrypted_file_encryption_key = file_encryption_key
        user.pub_key = pub_key
        user.encrypted_priv_key = priv_key

        user.s3_bucket_key = user.id
        user.set_password(hashlib.sha256(password.encode()).hexdigest())
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
	encrypted_file_encryption_key = models.TextField(max_length=2048,null=True)
	pub_key = models.TextField(max_length=4096,blank=False,unique=True,null=True)
	encrypted_priv_key = models.TextField(max_length=4096,blank=False,unique=True,null=True)
	pub_key = models.TextField(max_length=1024,blank=False,unique=True,null=False)
	real_size_used = models.IntegerField(default=0, blank=False,null=False)
	virtual_size_used = models.IntegerField(default=0, blank=False,null=False)
	virtual_size_limit = models.IntegerField(default=1000000, blank=False,null=False)
	s3_bucket = models.CharField(max_length=255,default='central')
	s3_bucket_key = models.CharField(max_length=255,null=False,unique=True)
	objects = UserManager()

	USERNAME_FIELD = 'email'

	

	
  

class Bucket(models.Model):

	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	owner = models.ForeignKey('User',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
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


class SharedEncryptionKey(models.Model):
	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	encrypted_key = models.TextField(null=False)
	created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='sender')
	created_for = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='receiver')	






	

