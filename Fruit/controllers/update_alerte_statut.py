from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Fruit.models import Alerte
from Fruit.serializers.update_alerte_statut import AlerteUpdateSerializer
from Systeme_Alerte.utils import my_answers
from django.shortcuts import get_object_or_404

class MarkAlertAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, alerte_id):
        alerte = get_object_or_404(Alerte, id=alerte_id)

        if alerte.utilisateur != request.user:
            etat = "ECHEC"
            msg = "Vous n'êtes pas autorisé à modifier cette alerte."
            res = my_answers(etat, msg, "Accès refusé")
            return Response(res, status=403)

        serializer = AlerteUpdateSerializer(alerte, data={"statut_lecture": True}, partial=True)

        if serializer.is_valid():
            serializer.save()
            etat = "SUCCES"
            msg = "Le statut de lecture de l'alerte a été mis à jour."
            res = my_answers(etat, msg, serializer.data)
            return Response(res)

        etat = "ECHEC"
        msg = "Erreur lors de la mise à jour de l'alerte."
        res = my_answers(etat, msg, serializer.errors)
        return Response(res, status=400)
