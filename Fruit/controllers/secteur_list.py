from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from Fruit.models import Secteur
from Fruit.serializers.secteur_list import SecteurListSerializer
from Systeme_Alerte.utils import my_answers

class SecteurListView(generics.ListAPIView):
    queryset = Secteur.objects.all()
    serializer_class = SecteurListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        etat = "SUCCES"
        msg = "Liste des secteurs récupérée avec succès."
        
        return Response(my_answers(etat, msg, serializer.data))