from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('forms-api/', include('FORMS.urls')),
    path('site-api/', include('API.urls')),
    path('sms-api/', include('SMS.urls')),
    path('messenger-api/', include('MESSENGER.urls'))
]
