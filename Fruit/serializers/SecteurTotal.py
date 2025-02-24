from rest_framework import serializers
from Fruit.models import MaturationStats

class SecteurTotalMurSerializer(serializers.Serializer):
    secteur_id = serializers.IntegerField(source='secteur.id')
    secteur_nom = serializers.CharField(source='secteur.nom')
    total_mur = serializers.FloatField()

    class Meta:
        fields = ['secteur_id', 'secteur_nom', 'total_mur', 'mois']
