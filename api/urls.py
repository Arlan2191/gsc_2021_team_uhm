from os import name
from django.urls import path, re_path
from api.views import ApiView

urlpatterns = [
    path('GET/<table_name>/', ApiView.getRequest, name="getRequest"),
    re_path(r'^GET/(?P<table_name>(PI|TI|ES|VS))/(?P<id>[\d]+)?$',
            ApiView.getRequest, name="getRequest"),
    path('POST/<table_name>', ApiView.postRequest, name="postRequest"),
]
