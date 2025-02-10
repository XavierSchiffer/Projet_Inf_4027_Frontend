from rest_framework import serializers
from Fruit.models import Rapport

class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = [
            'id', 'secteur', 'etat_global', 'date_envoi',
            'quantite_recolte', 'commentaire',
            'pourcentage_papaye_mur', 'pourcentage_papaye_non_mur', 'pourcentage_papaye_semi_mur'
        ]
