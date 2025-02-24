from django.urls import path

from account.controllers.registration import RegistrationSAdminsAPIView, RegistrationGestAPIView
from account.controllers.login import LoginAdminAPIView
from account.controllers.list_User import NonAdminUserListView, AdminListView
from account.controllers.infoUser import UserInfoView
from account.controllers.updateUser import UpdateUserInfoView
from account.controllers.updatePass import ChangeUsersPasswordAPIView
from account.controllers.accountUsers import NonAdminUserCountView
from account.controllers.countAdmin import AdminUserCountView
from account.controllers.countSector import SecteurCountAPIView
from account.controllers.registration import RegistrationAdminAPIView

app_name = 'account'

urlpatterns = [
    path("admin/registration/admin", RegistrationSAdminsAPIView.as_view()),
    path("admin/registration/admin1", RegistrationAdminAPIView.as_view()),
    path("admin/registration/users", RegistrationGestAPIView.as_view()),
    path("login/admin", LoginAdminAPIView.as_view()),
    path('users/list', NonAdminUserListView.as_view(), name='non-admin-users'),
    path('admin/list', AdminListView.as_view(), name='admin'),
    path('users/info', UserInfoView.as_view(), name='info-users'),
    path('users/update', UpdateUserInfoView.as_view(), name='update-users'),
    path('users/update/pass', ChangeUsersPasswordAPIView.as_view(), name='update-users-password'),
    path("users/non_admin/count/", NonAdminUserCountView.as_view(), name="non_admin_user_count"),
    path("admin/count/", AdminUserCountView.as_view(), name="admin_user_count"),
    path("secteurs/count/", SecteurCountAPIView.as_view(), name="secteur-count"),

]