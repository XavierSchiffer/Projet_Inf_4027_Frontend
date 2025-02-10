from rest_framework import serializers
from Fruit.models import User

class NonAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nom', 'prenom', 'telephone', 'email', 'role']
