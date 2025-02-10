from rest_framework import serializers
from Fruit.models import Secteur
from account.models import User

class SecteurSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)

    class Meta:
        model = Secteur
        fields = ['nom', 'username']

    def create(self, validated_data):
        username = validated_data.pop('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username": "Cet utilisateur n'existe pas."})

        if hasattr(user, 'secteurs'):
            raise serializers.ValidationError({"username": "Cet utilisateur a déjà un secteur."})

        return Secteur.objects.create(utilisateur=user, **validated_data)
