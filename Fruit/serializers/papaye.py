# from rest_framework import serializers
# from Fruit.models import Papaye, Secteur

# class PapayeSerializer(serializers.ModelSerializer):
#     secteur = serializers.PrimaryKeyRelatedField(queryset=Secteur.objects.all(), required=True)

#     class Meta:
#         model = Papaye
#         fields = ["id", "secteur", "image", "stade_maturation", "date_derniere_analyse"]
#         read_only_fields = ["stade_maturation"]  # Ces champs seront définis par l'IA

#     def validate_secteur(self, value):
#         """Vérifie que l'utilisateur connecté gère bien ce secteur."""
#         request = self.context.get("request")
#         if request and request.user and value.utilisateur != request.user:
#             raise serializers.ValidationError("Vous n'êtes pas autorisé à ajouter une papaye dans ce secteur.")
#         return value

from rest_framework import serializers
from Fruit.models import Papaye, Secteur

class PapayeSerializer(serializers.ModelSerializer):
    # secteur = serializers.PrimaryKeyRelatedField(queryset=Secteur.objects.all(), required=True)

    class Meta:
        model = Papaye
        fields = [
            "id", 
            "secteur", 
            "image", 
            # "stade_maturation", 
            "date_derniere_analyse"
        ]
        # read_only_fields = ["stade_maturation"]  # Ces champs seront définis par l'IA

class PapayeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Papaye
        fields = ["stade_maturation"]

    def update(self, instance, validated_data):
        old_maturation = instance.stade_maturation
        new_maturation = validated_data.get("stade_maturation", instance.stade_maturation)

          # Vérifie si le stade change
        if old_maturation != new_maturation:
            instance.stade_maturation = new_maturation
            instance.save()
        return instance
