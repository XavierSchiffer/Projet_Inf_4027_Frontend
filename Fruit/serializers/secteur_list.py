from rest_framework import serializers
from Fruit.models import Secteur

class SecteurListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="utilisateur.username", read_only=True)

    class Meta:
        model = Secteur
        fields = ['id', 'nom', 'username']
