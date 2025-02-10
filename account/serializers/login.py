from rest_framework import serializers

from account.models import User


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=2,
    )
    username = serializers.CharField()
    # token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username:
            raise serializers.ValidationError("Le nom d'utilisateur est requis.")
        
        if not password:
            raise serializers.ValidationError("Le mot de passe est requis.")

        return {
            'username': username,
            'password': password,
        }
    
    class Meta:
        model = User
        fields = ['username', 'password']
