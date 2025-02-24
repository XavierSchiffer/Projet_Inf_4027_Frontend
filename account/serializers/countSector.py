from rest_framework import serializers
# from Fruit.models import Secteur

class SecteurCountSerializer(serializers.Serializer):
    nombre_secteurs = serializers.IntegerField()