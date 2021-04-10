from django.urls import path, re_path
from .views import RegistrationAPIView, LoginAPIView, AuthUserRetrieveUpdateAPIView

urlpatterns = [
    # re_path(r'^users/?$', RegistrationAPIView.as_view()),
    re_path(r'^users/login/?$', LoginAPIView.as_view()),
    re_path(r'^user/?$', AuthUserRetrieveUpdateAPIView.as_view()),
]
