from django.urls import path, include
from accounts.api.v1 import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

# from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    # registration
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),

    # activation
    # path('activation/confirm/', views.TestEmailSend.as_view() , name='email-test'),
    
    path('activation/confirm/<str:token>', views.ActivationApiView.as_view() , name='activation'),

    # resend activation
    path('activation/resend/',views.ResendActivationEmailApiView.as_view(), name='resend-activation'),

    # change password
    path('change-password/',views.ChangePasswordApiView.as_view(), name='change-password'),
    

    # login token
    path('token/login', views.ObtainAuthTokenView.as_view(), name='token-login'),
    path('token/logout', views.CustomDiscardAuthToken.as_view(), name='token-logout'),


    # login jwt
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    
]
