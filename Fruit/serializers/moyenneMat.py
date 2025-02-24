from rest_framework import serializers
from Fruit.models import MaturationStats

class MaturationStatsSerializer(serializers.ModelSerializer):
    moyenne_non_mur = serializers.ReadOnlyField()
    moyenne_semi_mur = serializers.ReadOnlyField()
    moyenne_mur = serializers.ReadOnlyField()

    class Meta:
        model = MaturationStats
        fields = ['secteur', 'moyenne_non_mur', 'moyenne_semi_mur', 'moyenne_mur']