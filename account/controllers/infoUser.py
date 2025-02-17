from rest_framework import  permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.contrib.auth.models import User
from account.serializers.infoUser import UserSerializer

class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        
        response_data = {
            "etat": 'SUCCES',
            "msg": "Informations de l'utilisateur connecté",
            "res": serializer.data
        }
        
        return Response(response_data)
