from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Fruit.models import MaturationStats
from Systeme_Alerte.utils import my_answers
from Fruit.serializers.SecteurTotal import SecteurTotalMurSerializer
from decimal import Decimal
from Fruit.models import Secteur
class SecteursTopMurAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer les 3 secteurs avec les total_mur les plus élevés
        secteurs_top = MaturationStats.objects.all().order_by('-total_mur')[:3]

        if not secteurs_top:
            etat = "ECHEC"
            msg = "Aucun secteur n'a été trouvé."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=400)

        # Serializer les secteurs
        serializer = SecteurTotalMurSerializer(secteurs_top, many=True)

        etat = "SUCCES"
        msg = "Secteurs récupérés avec succès."
        res = my_answers(etat, msg, serializer.data)
        return Response(res)



class MaturationParSecteurAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer le secteur de l'utilisateur connecté
        secteur = Secteur.objects.filter(utilisateur=request.user).first()

        if not secteur:
            etat = "ECHEC"
            msg = "Aucun secteur assigné à cet utilisateur."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=400)

        # Récupérer les statistiques de maturation pour ce secteur
        stats = MaturationStats.objects.filter(secteur=secteur).first()

        if not stats:
            etat = "ECHEC"
            msg = "Aucune donnée de maturation trouvée pour ce secteur."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=404)

        # Calculer les pourcentages de maturation pour le secteur
        total_papayes = stats.total_non_mur + stats.total_semi_mur + stats.total_mur
        if total_papayes > 0:
            taux_maturation = (stats.total_mur / total_papayes) * 100
        else:
            taux_maturation = 0

        result = {
            'secteur_id': stats.secteur.id,
            'secteur_nom': stats.secteur.nom,
            'taux_maturation': round(taux_maturation, 2)
        }

        etat = "SUCCES"
        msg = "Le taux de maturation pour ce secteur a été récupéré avec succès."
        res = my_answers(etat, msg, result)
        return Response(res)
    

class TauxMaturationMoyenParMoisAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer le mois demandé depuis les paramètres de la requête
        mois = request.query_params.get('mois', None)

        if not mois:
            etat = "ECHEC"
            msg = "Le mois doit être fourni dans la requête."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=400)

        # Récupérer les statistiques de maturation et calculer le taux moyen pour ce mois
        stats = MaturationStats.objects.filter(mois=mois)

        if not stats:
            etat = "ECHEC"
            msg = "Aucune donnée de maturation trouvée pour ce mois."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=404)

        # Calcul du taux moyen de maturation pour le mois
        moyenne_maturation = stats.aggregate(
            moyenne=Avg('total_mur')
        )['moyenne']

        result = {
            'mois': mois,
            'moyenne_maturation': round(moyenne_maturation, 2) if moyenne_maturation else 0
        }

        etat = "SUCCES"
        msg = "Le taux de maturation moyen pour le mois a été récupéré avec succès."
        res = my_answers(etat, msg, result)
        return Response(res)


class SecteursTopMaturationParMoisAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer le mois demandé depuis les paramètres de la requête
        mois = request.query_params.get('mois', None)

        if not mois:
            etat = "ECHEC"
            msg = "Le mois doit être fourni dans la requête."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=400)

        # Filtrer les MaturationStats pour le mois spécifié et trier par 'total_mur' en ordre décroissant
        secteurs_stats = MaturationStats.objects.filter(mois=mois).order_by('-total_mur')[:3]

        if not secteurs_stats:
            etat = "ECHEC"
            msg = "Aucun secteur trouvé pour ce mois."
            res = my_answers(etat, msg, "erreur")
            return Response(res, status=404)

        # Préparer les résultats
        result = []
        for stats in secteurs_stats:
            result.append({
                'secteur_id': stats.secteur.id,
                'secteur_nom': stats.secteur.nom,
                'total_mur': stats.total_mur
            })

        etat = "SUCCES"
        msg = "Les 3 meilleurs secteurs pour le mois ont été récupérés avec succès."
        res = my_answers(etat, msg, result)
        return Response(res)
