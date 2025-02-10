from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Fruit.models import Alerte
from Fruit.serializers.detail_alerte import AlerteDetailSerializer
from Systeme_Alerte.utils import my_answers
from django.shortcuts import get_object_or_404

class AlerteDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, alerte_id):
        alerte = get_object_or_404(Alerte, id=alerte_id)

        serializer = AlerteDetailSerializer(alerte)

        etat = "SUCCES"
        msg = "Détails de l'alerte récupérés avec succès."
        res = my_answers(etat, msg, serializer.data)

        return Response(res)
