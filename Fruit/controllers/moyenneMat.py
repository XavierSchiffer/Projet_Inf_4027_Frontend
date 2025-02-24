from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Fruit.models import MaturationStats
from Fruit.serializers.moyenneMat import MaturationStatsSerializer
from Fruit.models import Secteur

class MaturationStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer le secteur de l'utilisateur
        secteur = Secteur.objects.filter(utilisateur=request.user).first()

        if not secteur:
            return Response({"error": "Aucun secteur assigné à cet utilisateur."}, status=404)

        # Récupérer les statistiques de maturation pour ce secteur
        stats = MaturationStats.objects.filter(secteur=secteur).first()

        if not stats:
            return Response({"error": "Aucune donnée de maturation disponible pour ce secteur."}, status=404)

        serializer = MaturationStatsSerializer(stats)
        return Response(serializer.data)