from rest_framework import serializers
from Fruit.models import Alerte

class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = "__all__"
