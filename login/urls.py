from django.urls import path
from login.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegistrationView.as_view(), name = 'register'), #not yet used
    # TODO: Fix double login in the url.
    path('login/', obtain_auth_token, name = 'login'),  #this has been used
    path('UserData/', UserDataView.as_view(), name = 'UserData'),  #this has been used
    path('PasswordReset/', PasswordReset.as_view() ,name = "Change Password"),  #This has been used.
]
