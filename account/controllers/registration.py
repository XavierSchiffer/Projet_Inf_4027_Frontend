from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers.registration import RegistrationAdminsSerializer,RegistrationGestSerializer
from Systeme_Alerte.utils import my_answers
from drf_yasg.utils import swagger_auto_schema

class RegistrationSAdminsAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationAdminsSerializer

    @swagger_auto_schema(request_body=RegistrationAdminsSerializer)
    def post(self, request):
    
        Admins_query = {
            'nom': request.data["nom"], 
            'prenom': request.data["prenom"], 
            'password': request.data["password"], 
            'username': request.data["username"],
            'email': request.data["email"],
            'role': "ADMIN", 
        }

        print("#########", Admins_query)
        serializer = self.serializer_class(data = Admins_query)
        serializer.is_valid(raise_exception=True)
        serializer.save()
   
        etat = "SUCCES"
        msg = "Admins enregistré avec succès"
        res = my_answers(etat,msg , serializer.data,)
        return Response(res)

class RegistrationAdminAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationAdminsSerializer

    @swagger_auto_schema(request_body=RegistrationAdminsSerializer)
    def post(self, request):
        print("En-têtes reçus :", request.headers)
        if request.user.is_authenticated:
            if request.user.role == "ADMIN":
                Admins_query = {
                    'nom': request.data["nom"], 
                    'prenom': request.data["prenom"], 
                    'email': request.data["email"], 
                    'telephone': request.data["telephone"],
                    # 'role': request.data["role"],

                }

                print("#########", Admins_query)

                nom = Admins_query["nom"].split(" ")
                prenom = Admins_query["prenom"].split(" ")
                # role = "ADMIN"
                Admins_save = {
                    'nom': request.data["nom"], 
                    'prenom': request.data["prenom"], 
                    'password': "admin-" + prenom[0], 
                    'username': prenom[0] + '.' + nom[0],
                    'email': request.data["email"],
                    'role': "ADMIN", 
                    'telephone': request.data["telephone"], 
                }
                serializer = self.serializer_class(data = Admins_save)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        
                etat = "SUCCES"
                msg = "Admin enregistré avec succès"
                res = my_answers(etat,msg , serializer.data,)
                return Response(res)
            else:
                 etat = "ECHEC"
                 msg = "Vous ne pouvez pas effectuer cette action"
                 res = my_answers(etat, msg, "No Data")
                 return Response(res)
        etat = "ECHEC"
        msg = "Utilisateur non authentifié"
        res = my_answers(etat, msg, "No Data")
        return Response(res)


class RegistrationGestAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationGestSerializer

    @swagger_auto_schema(request_body=RegistrationGestSerializer)
    def post(self, request):
        print("En-têtes reçus :", request.headers)
        if request.user.is_authenticated:
            if request.user.role == "ADMIN":
                Admins_query = {
                    'nom': request.data["nom"], 
                    'prenom': request.data["prenom"], 
                    'email': request.data["email"], 
                    'telephone': request.data["telephone"],
                    'role': request.data["role"],

                }

                print("#########", Admins_query)

                nom = Admins_query["nom"].split(" ")
                prenom = Admins_query["prenom"].split(" ")
        
                Admins_save = {
                    'nom': request.data["nom"], 
                    'prenom': request.data["prenom"], 
                    'password': "users-" + prenom[0], 
                    'username': prenom[0] + '.' + nom[0],
                    'email': request.data["email"],
                    'role': request.data["role"], 
                    'telephone': request.data["telephone"], 
                }
                serializer = self.serializer_class(data = Admins_save)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        
                etat = "SUCCES"
                msg = "Gestionnaire enregistré avec succès"
                res = my_answers(etat,msg , serializer.data,)
                return Response(res)
            else:
                 etat = "ECHEC"
                 msg = "Vous ne pouvez pas effectuer cette action"
                 res = my_answers(etat, msg, "No Data")
                 return Response(res)
        etat = "ECHEC"
        msg = "Utilisateur non authentifié"
        res = my_answers(etat, msg, "No Data")
        return Response(res)