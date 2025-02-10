from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from Fruit.models import Rapport
from Fruit.serializers.list_rapport import RapportSerializer

class UserRapportListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rapports = Rapport.objects.filter(utilisateur=request.user).order_by('-date_envoi')
        serializer = RapportSerializer(rapports, many=True)

        response_data = {
            "state": "SUCCES",
            "message": "Liste des rapports récupérée avec succès.",
            "results": serializer.data
        }
        return Response(response_data)
