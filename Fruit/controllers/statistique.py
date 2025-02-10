from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from Fruit.models import StatistiqueRecolte, Secteur
from Fruit.serializers.statistique import StatistiqueRecolteSerializer
from Systeme_Alerte.utils import my_answers

class StatistiqueRecolteListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        secteur = Secteur.objects.filter(utilisateur=request.user).first()
        if not secteur:
            etat = "ECHEC"
            msg = "Aucun secteur assigné à cet utilisateur."
            res = my_answers(etat, msg, "erreur")
            return Response(res)

        stats = StatistiqueRecolte.objects.filter(secteur=secteur)

        if not stats.exists():
            etat = "ECHEC"
            msg = "Aucune donnée de statistique trouvée pour votre secteur."
            res = my_answers(etat, msg, "erreur")
            return Response(res)

        serializer = StatistiqueRecolteSerializer(stats, many=True)

        etat = "SUCCES"
        msg = "Statistiques récupérées avec succès."
        res = my_answers(etat, msg, serializer.data)
        return Response(res)
