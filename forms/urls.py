from os import name
from django.urls import path, re_path
from FORMS.views import FormsView

urlpatterns = [
    path('POST', FormsView.postRequest, name="postRequest"),
]
