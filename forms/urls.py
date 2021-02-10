from os import name
from django.urls import path, re_path
from .views import FormsView

urlpatterns = [
    path('GET/<table_name>/', FormsView.getRequest, name="getRequest"),
    re_path(r'^GET/(?P<table_name>(PI|TI|ES))/(?P<id>[\d]+)?$',
            FormsView.getRequest, name="getRequest"),
    path('POST', FormsView.postRequest, name="postRequest"),
]
