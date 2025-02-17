from rest_framework import serializers
from account.models import User

class UpdateUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "nom", "prenom", "email", "telephone"]

    def validate_username(self, value):
        """Désactive la validation automatique pour gérer l'erreur dans la vue"""
        request = self.context.get('request')  # Récupérer l'utilisateur connecté
        user = request.user if request else None

        if user and value != user.username and User.objects.filter(username=value).exists():
            raise serializers.ValidationError("CUSTOM_ERROR")  # Message générique pour le capturer dans la vue

        return value
