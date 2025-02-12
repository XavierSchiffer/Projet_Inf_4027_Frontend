from Systeme_Alerte.utils import my_answers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from Fruit.models import Papaye, Secteur
from Fruit.serializers.papaye import PapayeSerializer, PapayeUpdateSerializer

from django.utils.timezone import now
from Fruit.fonction.model import prediction_maturity_papaya
import os

from django.conf import settings


class PapayeCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PapayeSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        secteur = Secteur.objects.filter(utilisateur=request.user).first()
        if not secteur:
            return Response(my_answers("ECHEC", "Aucun secteur assigné à cet utilisateur.", "erreur"))
        
        try:
            papaye = Papaye.objects.get(secteur=secteur)
            ancien_stade_maturation = papaye.stade_maturation

            if "image" in request.data:
                papaye.image = request.data["image"]
                papaye.date_derniere_analyse = now()
                papaye.save()

                # Récupérer le chemin du projet Django
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

                # Construire dynamiquement le chemin du modèle
                MODEL_PATH = os.path.join(BASE_DIR, "Fruit", "models", "shape_classifier.h5")

                chemin = os.path.join(settings.MEDIA_ROOT, papaye.image.name)
                # chemin = f'C:/Users/Neymar_Jr/Documents/Projet_GL/Systeme_Alerte{papaye.image.url}'
                # stade_maturation_pred, probas = prediction_maturity_papaya(
                #     chemin, 
                #     'C:/Users/Neymar_Jr/Documents/Projet_GL/Systeme_Alerte/shape_classifier.h5'
                # )

                stade_maturation_pred, probas = prediction_maturity_papaya(chemin, MODEL_PATH)

                if stade_maturation_pred != ancien_stade_maturation:
                    papaye.stade_maturation = stade_maturation_pred
                
                total = sum(probas.values())
                papaye.pourcentage_papaye_non_mur = round((probas["non-mur"] / total) * 100, 2)
                papaye.pourcentage_papaye_semi_mur = round((probas["semi-mur"] / total) * 100, 2)
                papaye.pourcentage_papaye_mur = round((probas["mur"] / total) * 100, 2)
                papaye.save()

                action = "mise à jour"
            else:
                return Response(my_answers("ECHEC", "Aucune image fournie.", "Erreur"))
        except Papaye.DoesNotExist:
            data = request.data.copy()
            data["secteur"] = secteur.id
            serializer = self.serializer_class(data=data, context={"request": request})

            if serializer.is_valid():
                papaye = serializer.save(date_derniere_analyse=now())

                # chemin = f'C:/Users/Neymar_Jr/Documents/Projet_GL/Systeme_Alerte{papaye.image.url}'
                # stade_maturation_pred, probas = prediction_maturity_papaya(
                #     chemin, 
                #     'C:/Users/Neymar_Jr/Documents/Projet_GL/Systeme_Alerte/shape_classifier.h5'
                # )
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

                # Construire dynamiquement le chemin du modèle
                MODEL_PATH = os.path.join(BASE_DIR, "Fruit", "models", "shape_classifier.h5")

                chemin = os.path.join(settings.MEDIA_ROOT, papaye.image.name)
                stade_maturation_pred, probas = prediction_maturity_papaya(chemin, MODEL_PATH)

                papaye.stade_maturation = stade_maturation_pred
                total = sum(probas.values())
                papaye.pourcentage_papaye_non_mur = round((probas["non-mur"] / total) * 100, 2)
                papaye.pourcentage_papaye_semi_mur = round((probas["semi-mur"] / total) * 100, 2)
                papaye.pourcentage_papaye_mur = round((probas["mur"] / total) * 100, 2)
                papaye.save()

                action = "ajoutée"
            else:
                return Response(my_answers("ECHEC", "Erreur lors de l'ajout de la papaye.", serializer.errors))

        papaye_data = {
            "secteur": papaye.secteur.id,
            "image": papaye.image.url if papaye.image else None,
            "stade_maturation": papaye.stade_maturation,
            "date_derniere_analyse": papaye.date_derniere_analyse.strftime("%Y-%m-%d %H:%M:%S"),
            "pourcentage_papaye_non_mur": papaye.pourcentage_papaye_non_mur,
            "pourcentage_papaye_semi_mur": papaye.pourcentage_papaye_semi_mur,
            "pourcentage_papaye_mur": papaye.pourcentage_papaye_mur,
        }

        return Response(my_answers("SUCCES", f"Papaye {action} avec succès.", papaye_data))
# class PapayeCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PapayeSerializer

#     @swagger_auto_schema(request_body=serializer_class)
#     def post(self, request):
#         # Récupérer le secteur de l'utilisateur
#         secteur = Secteur.objects.filter(utilisateur=request.user).first()

#         if not secteur:
#             etat = "ECHEC"
#             msg = "Aucun secteur assigné à cet utilisateur."
#             res = my_answers(etat, msg, "erreur")
#             return Response(res)

#         try:
#             # Vérifier si une papaye existe déjà dans ce secteur
#             papaye = Papaye.objects.get(secteur=secteur)

#             # Mise à jour de l'image et de la date de la dernière analyse
#             if "image" in request.data:
#                 papaye.image = request.data["image"]
#                 papaye.date_derniere_analyse = now()
#                 papaye.save()

#                 # Obtenir le chemin de l'image mise à jour
#                 chemin = f'C:/Users/Neymar_Jr/Documents/Projet_GL/Systeme_Alerte{papaye.image.url}'

#                 # Prédire le stade de maturation
#                 stade_maturation_pred = prediction_maturity_papaya(
#                     chemin, 
#                     'C:/Users/Neymar_Jr/Documents/Projet_GL/Systeme_Alerte/shape_classifier.h5'
#                 )

#                 print("#######  Resultat de ma fonction de prediction :", stade_maturation_pred)
#                 stade_maturation_pred1 = "mur" 

#                 # Mise à jour du stade de maturation avec la valeur prédite
#                 papaye.stade_maturation = stade_maturation_pred1
#                 papaye.save()

#                 action = "mise à jour"
#             else:
#                 etat = "ECHEC"
#                 msg = "Aucune image fournie."
#                 res = my_answers(etat, msg, "Erreur")
#                 return Response(res)

#         except Papaye.DoesNotExist:
#             # Création d'une nouvelle papaye
#             data = request.data.copy()
#             data["secteur"] = secteur.id
#             serializer = self.serializer_class(data=data, context={"request": request})

#             if serializer.is_valid():
#                 papaye = serializer.save(date_derniere_analyse=now())

#                 # Obtenir le chemin de l'image
#                 chemin = f'C:/Users/Neymar_Jr/Documents/Projet_GL/Systeme_Alerte{papaye.image.url}'

#                 # Prédire le stade de maturation
#                 stade_maturation_pred = prediction_maturity_papaya(
#                     chemin, 
#                     'C:/Users/Neymar_Jr/Documents/Projet_GL/Systeme_Alerte/shape_classifier.h5'
#                 )

#                 # Mise à jour du stade de maturation
#                 papaye.stade_maturation = stade_maturation_pred
#                 papaye.save()

#                 action = "ajoutée"
#             else:
#                 etat = "ECHEC"
#                 msg = "Erreur lors de l'ajout de la papaye."
#                 res = my_answers(etat, msg, serializer.errors)
#                 return Response(res)

#         # Construire la réponse
#         papaye_data = {
#             "secteur": papaye.secteur.id,
#             "image": papaye.image.url if papaye.image else None,
#             "stade_maturation": papaye.stade_maturation,
#             "date_derniere_analyse": papaye.date_derniere_analyse.strftime("%Y-%m-%d %H:%M:%S"),
#         }

#         etat = "SUCCES"
#         msg = f"Papaye {action} avec succès."
#         res = my_answers(etat, msg, papaye_data)
#         return Response(res)




class PapayeUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Seuls les utilisateurs connectés peuvent modifier la papaye
    serializer_class = PapayeUpdateSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def patch(self, request, papaye_id):
        try:
            # Vérifier si la papaye existe et appartient à un secteur géré par l'utilisateur connecté
            papaye = Papaye.objects.get(id=papaye_id)

            if papaye.secteur.utilisateur != request.user:
                etat = "ECHEC"
                msg = "Vous n'êtes pas autorisé à modifier cette papaye."
                res = my_answers(etat, msg, "erreur")
                return Response(res)

        except Papaye.DoesNotExist:
            etat = "ECHEC"
            msg = "Papaye introuvable ou non autorisée."
            res = my_answers(etat, msg, "erreur")
            return Response(res)

        serializer = self.serializer_class(papaye, data=request.data, partial=True)
        if serializer.is_valid():
            # Déclenche le signal si `stade_maturation` change
            serializer.save()  

            etat = "SUCCES"
            msg = "Stade de maturation mis à jour avec succès."
            res = my_answers(etat, msg, serializer.data)
            return Response(res)
        
        etat = "ECHEC"
        msg = "Erreur lors de la mise à jour du stade de maturation."
        res = my_answers(etat, msg, serializer.errors)
        return Response(res)
