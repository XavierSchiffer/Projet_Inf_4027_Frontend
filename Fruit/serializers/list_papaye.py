from rest_framework import serializers
from Fruit.models import Papaye

class PapayeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Papaye
        fields = [
            'id', 'secteur', 'date_derniere_analyse',
            'pourcentage_papaye_mur', 'pourcentage_papaye_non_mur', 'pourcentage_papaye_semi_mur'
        ]
