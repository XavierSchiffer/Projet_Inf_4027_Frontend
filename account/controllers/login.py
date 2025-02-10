
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers.login import *
from django.contrib.auth import authenticate
from Systeme_Alerte.utils import my_answers

# Create your views here.

class LoginAdminAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        
        if user:
            logged = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'nom': user.nom,
                'prenom': user.prenom,
                'token': user.token,
                'role': user.role,
            }
            etat = "SUCCES"
            msg = "Utilisateur authentifié avec succès"
            res = my_answers(etat, msg, logged)
            return Response(res)
        else:
            etat = "ECHEC"
            msg = "Nom d'utilisateur ou mot de passe incorrect"
            res = my_answers(etat, msg, "erreur")
            return Response(res)