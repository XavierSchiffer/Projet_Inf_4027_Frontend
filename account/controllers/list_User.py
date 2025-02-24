from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Systeme_Alerte.utils import my_answers
from Fruit.models import User
from account.serializers.list_User import NonAdminUserSerializer, AdminSerializer

class NonAdminUserListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NonAdminUserSerializer

    def get(self, request):
        # Vérifier si l'utilisateur connecté est un administrateur
        if not request.user.role == 'ADMIN':
            etat = "ECHEC"
            msg = "Permission refusée. Seuls les administrateurs peuvent accéder à cette ressource."
            res = my_answers(etat, msg, [])
            return Response(res, status=403)

        # Récupérer les utilisateurs dont le rôle est différent de ADMIN
        non_admin_users = User.objects.exclude(role='ADMIN')
        serializer = self.serializer_class(non_admin_users, many=True)

        etat = "SUCCES"
        msg = "Liste des utilisateurs non-admins récupérée avec succès."
        res = my_answers(etat, msg, serializer.data)
        return Response(res)


class AdminListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSerializer

    def get(self, request):
        # Vérifier si l'utilisateur connecté est un administrateur
        if not request.user.role == 'ADMIN':
            etat = "ECHEC"
            msg = "Permission refusée. Seuls les administrateurs peuvent accéder à cette ressource."
            res = my_answers(etat, msg, [])
            return Response(res, status=403)

        # Récupérer les utilisateurs dont le rôle est différent de ADMIN
        admin = User.objects.filter(role='ADMIN')
        serializer = self.serializer_class(admin, many=True)

        etat = "SUCCES"
        msg = "Liste des utilisateurs admins récupérée avec succès."
        res = my_answers(etat, msg, serializer.data)
        return Response(res)