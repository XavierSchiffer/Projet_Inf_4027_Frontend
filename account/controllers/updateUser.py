from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import User
from account.serializers.updateUser import UpdateUsersSerializer
from Systeme_Alerte.utils import my_answers


class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        serializer = UpdateUsersSerializer(user, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            etat = "SUCCES"
            msg = "Informations mises à jour avec succès"
            res = my_answers(etat, msg, serializer.data)
            return Response(res)
        # Capture l'erreur spécifique du username
        errors = serializer.errors
        if "username" in errors:
            # Vérifie si l'erreur indique que le nom d'utilisateur existe déjà
            if "Utilisateur with this username already exists." in errors["username"]:
                etat = "ECHEC"
                msg = "Ce nom d'utilisateur est déjà pris."
                res = my_answers(etat, msg, "No data")
                return Response(res)
        etat = "ECHEC"
        msg = "Erreur de validation"
        res = my_answers(etat, msg, errors)
        return Response(res)