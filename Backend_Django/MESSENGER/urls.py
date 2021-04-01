from os import name
from django.urls import path, re_path
from MESSENGER.views import MessengerView

urlpatterns = [
    path('POST', MessengerView.postRequest, name="postRequest"),
    path('VERIFY', MessengerView.confirmMobileNumber,
         name="checkMobileNumberRequest")
]
