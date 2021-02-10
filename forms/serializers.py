from django.core.serializers import serialize
from django.db.models import fields
from rest_framework import serializers
from .models import Auth_Mobile_Number, Personal_Information, Eligibility_Status, Tracking_Information


class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal_Information
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "birthdate",
            "sex",
            "mobile_number",
            "home_address",
            "city",
            "barangay"
        ]


class AuthMobileNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth_Mobile_Number
        fields = [
            "mobile_number",
            "amount_entry"
        ]


class EligibilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eligibility_Status
        fields = [
            "id",
            "status",
        ]


class TrackingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking_Information
        fields = [
            "id",
            "first_vaccination_status",
            "first_vaccination_date",
            "first_vaccination_time",
            "first_vaccination_site",
            "first_vaccination_serial",
            "first_vaccination_status",
            "second_vaccination_date",
            "second_vaccination_time",
            "second_vaccination_site",
            "second_vaccination_serial",
        ]
