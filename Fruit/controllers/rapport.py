from Fruit.serializers.rapport import RapportSerializer
from Fruit.models import Secteur

from Systeme_Alerte.utils import my_answers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from Fruit.models import Secteur, Papaye


# class RapportCreateAPIView(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = RapportSerializer

#     def perform_create(self, serializer):
#         secteur = Secteur.objects.filter(utilisateur=self.request.user).first()
#         if not secteur:
#             raise ValidationError("Vous n'êtes pas assigné à un secteur.")
        
#         serializer.save(utilisateur=self.request.user, secteur=secteur)


# class RapportCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = RapportSerializer

#     @swagger_auto_schema(request_body=serializer_class)
#     def post(self, request):
#         secteur = Secteur.objects.filter(utilisateur=request.user).first()
#         if not secteur:
#             etat = "ECHEC"
#             msg = "Aucun secteur assigné à cet utilisateur."
#             res = my_answers(etat, msg, "erreur")
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)

#         serializer = self.serializer_class(data=request.data, context={"request": request})
#         if serializer.is_valid():
#             rapport = serializer.save(utilisateur=request.user, secteur=secteur)

#             rapport_data = {
#                 "id": rapport.id,
#                 "secteur": rapport.secteur.id,  
#                 "utilisateur": rapport.utilisateur.id,
#                 "etat_global": rapport.etat_global,
#                 "date_envoi": rapport.date_envoi.strftime("%Y-%m-%d %H:%M:%S"),
#                 "quantite_recolte": rapport.quantite_recolte,
#                 "commentaire": rapport.commentaire
#             }

#             etat = "SUCCES"
#             msg = "Rapport soumis avec succès."
#             res = my_answers(etat, msg, rapport_data)
#             return Response(res)
        
#         etat = "ECHEC"
#         msg = "Erreur lors de la soumission du rapport."
#         res = my_answers(etat, msg, serializer.errors)
#         return Response(res)

from django.utils.datastructures import MultiValueDict

class RapportCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RapportSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        # Vérifier si l'utilisateur a un secteur assigné
        secteur = Secteur.objects.filter(utilisateur=request.user).first()
        if not secteur:
            etat = "ECHEC"
            msg = "Aucun secteur assigné à cet utilisateur."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        # Récupérer la dernière papaye analysée du secteur
        papaye = Papaye.objects.filter(secteur=secteur).order_by('-date_derniere_analyse').first()
        if not papaye:
            etat = "ECHEC"
            msg = "Aucune papaye trouvée pour ce secteur."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        # Créer une copie mutable des données de la requête
        mutable_data = request.data.copy()
        mutable_data.update({
            "pourcentage_papaye_mur": papaye.pourcentage_papaye_mur,
            "pourcentage_papaye_non_mur": papaye.pourcentage_papaye_non_mur,
            "pourcentage_papaye_semi_mur": papaye.pourcentage_papaye_semi_mur
        })

        # Sérialisation et sauvegarde
        serializer = self.serializer_class(data=mutable_data, context={"request": request})
        if serializer.is_valid():
            rapport = serializer.save(utilisateur=request.user, secteur=secteur)

            # Construction de la réponse
            rapport_data = {
                "id": rapport.id,
                "secteur": rapport.secteur.id,
                "utilisateur": rapport.utilisateur.id,
                "etat_global": rapport.etat_global,
                "date_envoi": rapport.date_envoi.strftime("%Y-%m-%d %H:%M:%S"),
                "quantite_recolte": rapport.quantite_recolte,
                "commentaire": rapport.commentaire,
                "pourcentage_papaye_mur": rapport.pourcentage_papaye_mur,
                "pourcentage_papaye_non_mur": rapport.pourcentage_papaye_non_mur,
                "pourcentage_papaye_semi_mur": rapport.pourcentage_papaye_semi_mur,
            }

            etat = "SUCCES"
            msg = "Rapport soumis avec succès."
            res = my_answers(etat, msg, rapport_data)
            return Response(res)

        # Gestion des erreurs
        etat = "ECHEC"
        msg = "Erreur lors de la soumission du rapport."
        res = my_answers(etat, msg, serializer.errors)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
