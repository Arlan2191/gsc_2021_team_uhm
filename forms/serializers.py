from rest_framework import serializers
from forms.models import Auth_Mobile_Number, Personal_Information


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
