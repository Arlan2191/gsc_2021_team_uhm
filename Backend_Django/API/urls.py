from django.urls import path, re_path
from API.views import DashboardAPIView, SMSSubscriptionAPIView, SMSVerificationAPIView, DatastoreAPIView, PersonnelRegistrationAPIView, TestingAPIView

app_name = 'main'
urlpatterns = [
    re_path(r'^table/?$', DashboardAPIView.as_view()),
    re_path(r'^staff/?$', PersonnelRegistrationAPIView.as_view()),
    re_path(r'^datastore/?$', DatastoreAPIView.as_view()),
    re_path(r'^otp/?$', SMSVerificationAPIView.as_view()),
    re_path(r'^token/?$', SMSSubscriptionAPIView.as_view()),
    re_path(r'^test/?$', TestingAPIView.as_view()),
]
