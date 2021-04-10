from django.urls import path, re_path
from API.views import DashboardAPIView, LGURegistrationAPIView, NotificationAPIView, SMSSubscriptionAPIView, SMSVerificationAPIView, DatastoreAPIView

app_name = 'main'
urlpatterns = [
    re_path(r'^table/?$', DashboardAPIView.as_view()),
    re_path(r'^staff/?$', LGURegistrationAPIView.as_view()),
    re_path(r'^datastore/?$', DatastoreAPIView.as_view()),
    re_path(r'^otp/?$', SMSVerificationAPIView.as_view()),
    re_path(r'^token/?$', SMSSubscriptionAPIView.as_view()),
    re_path(r'^notify/?$', NotificationAPIView.as_view()),
]
