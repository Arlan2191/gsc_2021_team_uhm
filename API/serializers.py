from rest_framework import serializers
from API.models import Eligibility_Status, Tracking_Information, Vaccination_Site


class EligibilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eligibility_Status
        fields = [
            "id",
            "status",
        ]


class VaccinationSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination_Site
        fields = [
            "site_address",
            "barangay",
            "city"
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
