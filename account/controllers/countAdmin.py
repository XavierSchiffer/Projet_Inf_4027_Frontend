from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from account.serializers.countAdmin import AdminUserCountSerializer

User = get_user_model()

class AdminUserCountView(APIView):
    permission_classes = [IsAuthenticated]  # Accès réservé aux utilisateurs authentifiés

    def get(self, request):
        # Compter les utilisateurs ayant le rôle 'ADMIN'
        admin_count = User.objects.filter(role="ADMIN").count()
        
        # Structure de réponse respectant ton format
        response_data = {
            "state": "SUCCES",
            "results": [
                {
                    "nombre_utilisateurs_admin": admin_count
                }
            ]
        }
        
        return Response(response_data)
