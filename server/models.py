import uuid
import hashlib
from Crypto.PublicKey import RSA
from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework.authtoken.models import Token
from server.utils import user_util_generate_file_encryption_key
from server.utils import user_util_generate_encrypted_key_pair


class Bucket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('User', related_name='bucket_owner', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    saved_as = models.CharField(max_length=255, null=False, blank=False)
    size = models.IntegerField(blank=False, null=False, default=0)
    size_on_s3 = models.IntegerField(null=True)
    description = models.TextField(max_length=500, null=True)
    s3_bucket = models.CharField(max_length=255, default='bashlist-78')
    s3_bucket_key = models.CharField(max_length=255, null=True)
    encrypted = models.BooleanField(default=True)
    emailed_to = models.ManyToManyField('User', related_name='email_recs')
    email_link_available = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    shared_with = models.ManyToManyField('User', related_name='shared_with_users')
    available = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    def json_representation(self):
        if self.is_shared:
            s = "Shared"
        else:
            s = "Private"
        if self.encrypted:
            e = "Encrypted"
        else:
            e = "Server Encryption"

        r = '{}/{}'.format(s, e)

        return {
            'Name': self.name,
            'Size': self.size,
            'Updated': self.updated_at,
            'Description': self.description,
            'Status': r
        }


class ActivityLog(models.Model):
    ACTIVITY_TYPES = (
        ('Do', 'Downloaded'),
        ('Up', 'Uploaded'),
        ('De', 'Deleted'),
        ('Sh', 'Shared'),
        ('Em', 'Emailed')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', null=False, editable=False, on_delete=models.CASCADE)
    bucket = models.ForeignKey('Bucket', null=False, editable=False, on_delete=models.CASCADE)
    action = models.CharField(max_length=2, choices=ACTIVITY_TYPES)


class SharedEncryptionKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    enrypted_bucket_encryption_key = models.TextField(max_length=4096,
                                                      null=False)  # key is encrypted by key_owner's public key
    bucket = models.ForeignKey('Bucket', on_delete=models.CASCADE)
    key_owner = models.ForeignKey('User', on_delete=models.CASCADE)


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
        pub_key, priv_key = user_util_generate_encrypted_key_pair(password)
        file_encryption_key = user_util_generate_file_encryption_key(password)
        user.encrypted_bucket_encryption_key = file_encryption_key
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
    email = models.EmailField(max_length=255, blank=False, unique=True, null=False)
    verified = models.BooleanField(default=False, blank=False)
    encrypted_bucket_encryption_key = models.TextField(max_length=2048, null=True)
    encrypted_priv_key = models.TextField(max_length=4096, blank=False, unique=True, null=True)
    pub_key = models.TextField(max_length=4096, blank=False, unique=True, null=False)
    real_size_used = models.IntegerField(default=0, blank=False, null=False)
    virtual_size_used = models.IntegerField(default=0, blank=False, null=False)
    virtual_size_limit = models.IntegerField(default=500000, blank=False, null=False)  # in KB
    s3_bucket = models.CharField(max_length=255, default='central')
    s3_bucket_key = models.CharField(max_length=255, null=False, unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def generate_account_url(self):
        return "https://www.google.com"
