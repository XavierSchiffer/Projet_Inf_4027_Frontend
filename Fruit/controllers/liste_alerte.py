from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Fruit.models import Alerte
from Fruit.serializers.list_alerte import AlerteSerializer


class UserUnreadAlertListView(APIView):
    """
    Récupère la liste des alertes non lues ou non traitées de l'utilisateur connecté.
    """
    permission_classes = [IsAuthenticated]  # L'utilisateur doit être authentifié

    def get(self, request):
        utilisateur = request.user  # Récupérer l'utilisateur connecté

        # Filtrer les alertes où statut_lecture=False ou statut=False
        alertes = Alerte.objects.filter(
            utilisateur=utilisateur,
            statut_lecture=False  # Si ton modèle contient "statut_lecture"
        ) .order_by('-date_envoi')  # Trier par date (récente en premier)

        alertes_data = []
        for alerte in alertes.distinct():
            alertes_data.append({
                "id": alerte.id,
                "message": alerte.message,
                "date_envoi": alerte.date_envoi.strftime("%Y-%m-%d %H:%M:%S"),
                "statut": alerte.statut,
                "statut_lecture": alerte.statut_lecture,
                "type_notification": alerte.type_notification
            })

        return Response({
            "status": "SUCCES",
            "message": "Liste des alertes récupérée avec succès.",
            "alertes": alertes_data
        })
