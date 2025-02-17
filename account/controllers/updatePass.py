from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password, make_password
from Systeme_Alerte.utils import my_answers
from account.models import User


class ChangeUsersPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.is_authenticated:
            # print("Données reçues:", request.data)  # 🔍 Debugging
            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')  # 🔹 Ajout du champ
            if not (current_password and new_password and confirm_password):
                etat = "ECHEC"
                msg = "Tous les champs (actuel, nouveau et confirmation) sont requis"
                res = my_answers(etat, msg, "No Data")
                return Response(res)
            if new_password != confirm_password:  # 🔹 Vérification de correspondance
                etat = "ECHEC"
                msg = "Le nouveau mot de passe et la confirmation ne correspondent pas"
                res = my_answers(etat, msg, "No Data")
                return Response(res)
            user = request.user
            if not check_password(current_password, user.password):
                etat = "ECHEC"
                msg = "Le mot de passe actuel est incorrect"
                res = my_answers(etat, msg, "No Data")
                return Response(res)
            user.password = make_password(new_password)
            user.save()
            etat = "SUCCES"
            msg = "Mot de passe mis à jour avec succès"
            res = my_answers(etat, msg, "No Data")
            return Response(res)
        etat = "ECHEC"
        msg = "Utilisateur non autorisé ou non authentifié"
        res = my_answers(etat, msg, "No Data")
        return Response(res)
