from os import name
from django.urls import path, re_path
from forms.views import FormsView

urlpatterns = [
    path('POST', FormsView.postRequest, name="postRequest"),
]
