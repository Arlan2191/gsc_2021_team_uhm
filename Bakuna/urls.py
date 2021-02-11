from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('forms-api/', include('forms.urls')),
    path('site-api/', include('api.urls'))
]
