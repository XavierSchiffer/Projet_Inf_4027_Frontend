from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from Fruit.serializers.secteur import SecteurSerializer
from Systeme_Alerte.utils import my_answers
# from django.contrib.auth.models import User
from account.models import User

class SecteurCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]  # L'utilisateur doit être connecté
    serializer_class = SecteurSerializer

    def post(self, request):
        # Vérifier si l'utilisateur est un administrateur
        if not request.user.role == "ADMIN":
            etat = "ECHEC"
            msg = "Accès refusé. Seuls les administrateurs peuvent effectuer cette action."
            return Response(my_answers(etat, msg, 'No data'))

        serializer = SecteurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # secteur = serializer.save()
            etat = "SUCCES"
            msg = f"L'utilisateur a été assigné au secteur avec succès."
            return Response(my_answers(etat, msg, serializer.data))

            # return Response(serializer.data, status=status.HTTP_201_CREATED)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        etat = "ECHEC"
        msg = "Erreur lors de l'assignation du secteur."
        return Response(my_answers(etat, msg, serializer.errors))


