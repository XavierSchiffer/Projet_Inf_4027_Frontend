from rest_framework import serializers
from Fruit.models import Alerte

class AlerteDetailSerializer(serializers.ModelSerializer):
    # utilisateur_nom = serializers.CharField(source="utilisateur.nom", read_only=True)
    # utilisateur_email = serializers.CharField(source="utilisateur.email", read_only=True)
    # papaye_id = serializers.IntegerField(source="papaye.id", read_only=True)

    class Meta:
        model = Alerte
        fields = ["id", "message", "type_notification", "statut", "date_envoi"]
