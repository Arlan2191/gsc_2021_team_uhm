from os import name
from django.urls import path, re_path
from SMS.views import SMSView

urlpatterns = [
    path('POST/RS', SMSView.receiveSMS, name="smsRequest"),
]
