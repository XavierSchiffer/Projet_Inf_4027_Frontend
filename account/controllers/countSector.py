from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Fruit.models import Secteur
from account.serializers.countSector import SecteurCountSerializer
from Systeme_Alerte.utils import my_answers  # Assure-toi que `my_answers` est bien défini

class SecteurCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nombre_secteurs = Secteur.objects.count()
        data = {"nombre_secteurs": nombre_secteurs}
        serializer = SecteurCountSerializer(data)
        
        return Response(my_answers("SUCCES", "Nombre total de secteurs récupéré avec succès.", serializer.data))
