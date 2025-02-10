from rest_framework import serializers
from account.models import User

class RegistrationAdminsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=2,
        # write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['id',
                  'nom',
                  'prenom',
                  'username', 
                  'password',
                  'email',
                  'role',
                  'token']

    def create(self, validated_data):
        admin = User.objects.create_user(**validated_data)
        return admin

class RegistrationGestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=2,
        # write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['id',
                  'nom',
                  'prenom',
                  'username', 
                  'password',
                  'email',
                  'role',
                  'telephone',
                  'token']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
