from rest_framework import serializers
from Fruit.models import StatistiqueRecolte


class StatistiqueRecolteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatistiqueRecolte
        fields = "__all__"
