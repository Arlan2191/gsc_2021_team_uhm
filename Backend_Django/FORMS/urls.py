from os import name
from django.urls import path, re_path
from FORMS.views import FormsAPIView

urlpatterns = [
    re_path(r'^submit/?$', FormsAPIView.as_view()),
]
