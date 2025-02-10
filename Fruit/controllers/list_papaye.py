from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Fruit.models import Papaye, Secteur
from Fruit.serializers.list_papaye import PapayeListSerializer
from Systeme_Alerte.utils import my_answers

class UserPapayeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer le secteur de l'utilisateur connecté
        secteur = Secteur.objects.filter(utilisateur=request.user).first()

        if not secteur:
            etat = "ECHEC"
            msg = "Aucun secteur assigné à cet utilisateur."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=400)

        # Récupérer les papayes de ce secteur
        papayes = Papaye.objects.filter(secteur=secteur)
        serializer = PapayeListSerializer(papayes, many=True)

        etat = "SUCCES"
        msg = "Liste des papayes récupérée avec succès."
        res = my_answers(etat, msg, serializer.data)
        return Response(res)
