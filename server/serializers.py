from .models import IndividualEncryptionKey
from rest_framework import serializers

class IndividualEncryptionKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualEncryptionKey
        fields = ('encrypte_key', 'created_by', 'created_for')
