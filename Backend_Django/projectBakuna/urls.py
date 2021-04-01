from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('AUTH.urls')),
    path('forms/', include('FORMS.urls')),
    path('site/', include('API.urls', namespace='main')),
    path('sms/', include('SMS.urls')),
    path('messenger/', include('MESSENGER.urls'))
]
