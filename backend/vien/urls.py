from django.urls import path
from .views import *

urlpatterns = [
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('send-phone-otp/', send_numotp, name='send_phone_otp'),
    path('verify-phone-otp/', verify_numotp, name='verify_phone_otp'),
    path('login/', login_user, name='login_user'),
     path('send-reset-otp/', send_reset_otp, name='send_reset_otp'),
    path('verify-reset-otp/', verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', reset_password, name='reset_password'),
]
