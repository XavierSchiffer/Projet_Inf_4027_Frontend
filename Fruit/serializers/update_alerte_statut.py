from rest_framework import serializers
from Fruit.models import Alerte

class AlerteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = ["statut_lecture"]

    def update(self, instance, validated_data):
        instance.statut_lecture = validated_data.get("statut_lecture", instance.statut_lecture)
        instance.save()
        return instance
