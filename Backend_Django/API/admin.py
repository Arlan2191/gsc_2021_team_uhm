from django.contrib import admin
from .models import Auth_Mobile_Number, AuthUser, Personal_Information, Personnel_Information, Eligibility_Status, Tracking_Information, Vaccination_Site

admin.register(Auth_Mobile_Number, AuthUser, Personal_Information,
               Personnel_Information, Eligibility_Status, Tracking_Information, Vaccination_Site)
