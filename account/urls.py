from django.urls import path

from account.controllers.registration import RegistrationSAdminsAPIView, RegistrationGestAPIView
from account.controllers.login import LoginAdminAPIView
from account.controllers.list_User import NonAdminUserListView

app_name = 'account'

urlpatterns = [
    path("admin/registration/admin", RegistrationSAdminsAPIView.as_view()),
    path("admin/registration/users", RegistrationGestAPIView.as_view()),
    path("login/admin", LoginAdminAPIView.as_view()),
    path('users/list', NonAdminUserListView.as_view(), name='non-admin-users'),
]