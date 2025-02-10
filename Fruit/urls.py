from django.urls import path
from Fruit.controllers.secteur import SecteurCreateAPIView
from Fruit.controllers.papaye import PapayeCreateAPIView, PapayeUpdateAPIView
from Fruit.controllers.alerte import MarkAlertAsReadAPIView
from Fruit.controllers.rapport import RapportCreateAPIView
from Fruit.controllers.statistique import StatistiqueRecolteListAPIView
from Fruit.controllers.liste_alerte import UserUnreadAlertListView
from Fruit.controllers.detail_alerte import AlerteDetailAPIView
from Fruit.controllers.list_rapport import UserRapportListView
from Fruit.controllers.list_papaye import UserPapayeListAPIView
from Fruit.controllers.secteur_list import SecteurListView

app_name = 'Fruit'

urlpatterns = [
    path('secteurs/create/', SecteurCreateAPIView.as_view(), name='create_secteur'),
    path('secteurs/papaye/upload/', PapayeCreateAPIView.as_view(), name='check_papaye'),
    path('secteurs/list/', SecteurListView.as_view(), name='list-secteur'),
    path('update/<int:papaye_id>/', PapayeUpdateAPIView.as_view(), name='update_papaye'),
    path('alertes/read/<int:alerte_id>/', MarkAlertAsReadAPIView.as_view(), name='mark_alert_as_read'),
    path("secteurs/papaye/rapports/", RapportCreateAPIView.as_view(), name="ajouter_rapport"),
    path("secteurs/papaye/stat/", StatistiqueRecolteListAPIView.as_view(), name="statistique_recolte"),
    path('alertes/non_lues/', UserUnreadAlertListView.as_view(), name='user-alerts'),
    path('alertes/<int:alerte_id>/', AlerteDetailAPIView.as_view(), name='alerte_detail'),
    path('rapports/list/', UserRapportListView.as_view(), name='user-rapport-list'),
    path('papayes/list/', UserPapayeListAPIView.as_view(), name='user_papaye_list'),



]
