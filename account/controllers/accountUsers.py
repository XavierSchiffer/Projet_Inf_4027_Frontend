from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from account.serializers.countUsers import NonAdminUserCountSerializer

User = get_user_model()

class NonAdminUserCountView(APIView):
    permission_classes = [IsAuthenticated]  # Protection avec authentification requise

    def get(self, request):
        # Compter les utilisateurs dont le rôle est différent de 'ADMIN'
        user_count = User.objects.exclude(role="ADMIN").count()
        
        # Structure de la réponse conforme à ton style
        response_data = {
            "state": "SUCCES",
            "results": [
                {
                    "nombre_utilisateurs": user_count
                }
            ]
        }
        
        return Response(response_data)