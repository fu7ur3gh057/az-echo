from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import RegisterAPIView, VerifyEmailAPIView, MyTokenObtainPairView, UpdatePasswordAPIView, \
    ResetPasswordRequestAPIView, SetNewPasswordAPIView, delete_user, LogoutAPIView,lol

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('email-verify/', VerifyEmailAPIView.as_view(), name='email-verify'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('update-password/', UpdatePasswordAPIView.as_view(), name='update_password'),
    path('reset-password', ResetPasswordRequestAPIView.as_view(), name='reset_password'),
    path('set-password', SetNewPasswordAPIView.as_view(), name='add_new_password'),
    path('delete/', delete_user, name='delete'),
    path('lol/', lol, name='delete'),
]
