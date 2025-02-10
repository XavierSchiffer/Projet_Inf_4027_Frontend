# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from Fruit.models import Alerte
# from Systeme_Alerte.utils import my_answers

# class MarkAlertAsReadAPIView(APIView):
#     def get(self, request, alerte_id):
#         try:
#             alerte = Alerte.objects.get(id=alerte_id)
#             alerte.statut_lecture = True
#             alerte.save()

#             etat = "SUCCES"
#             msg = "Alerte marquée comme lue."
#             res = my_answers(etat, msg, {"alerte_id": alerte.id, "statut_lecture": alerte.statut_lecture})
#             return Response(res)
        
#         except Alerte.DoesNotExist:
#             etat = "ECHEC"
#             msg = "Alerte introuvable."
#             res = my_answers(etat, msg, "erreur")
#             return Response(res)
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
from Fruit.models import Alerte
from Systeme_Alerte.utils import my_answers

class MarkAlertAsReadAPIView(APIView):
    def put(self, request, alerte_id):
        print(f"Requête reçue pour l'alerte {alerte_id}")

        try:
            alerte = Alerte.objects.get(id=alerte_id)
            print(f"Alerte trouvée : {alerte}")

            alerte.statut_lecture = True
            alerte.save()
            print(f"Alerte {alerte_id} marquée comme lue")

            etat = "SUCCES"
            msg = "Alerte marquée comme lue."
            res = my_answers(etat, msg, {"alerte_id": alerte.id, "statut_lecture": alerte.statut_lecture})
            return Response(res)

        except Alerte.DoesNotExist:
            print("Alerte introuvable")  # DEBUG
            etat = "ECHEC"
            msg = "Alerte introuvable."
            res = my_answers(etat, msg, "erreur")
            return Response(res)
