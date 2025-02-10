from rest_framework import serializers
from Fruit.models import Rapport

class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = "__all__"
        read_only_fields = ["utilisateur", "secteur", "date_envoi"]

