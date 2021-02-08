from django.urls import path
from .views import PhoneNumberAuthentication

urlpatterns = [
    path('<phone>/', PhoneNumberAuthentication.as_view(), name="Time Base OTP"),
]
