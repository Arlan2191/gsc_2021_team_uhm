from rest_framework import serializers
from API.models import Eligibility_Status, Tracking_Information, Vaccination_Site


class EligibilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eligibility_Status
        fields = [
            "id",
            "status",
            "reason",
        ]

    def update(self, instance, validated_data):
        if validated_data.get("status") != "None" or validated_data.get("status") != "":
            instance.status = validated_data.get("status", instance.status)
        if validated_data.get("reason") != "None" or validated_data.get("reason") != "":
            instance.status = validated_data.get("reason", instance.status)
        instance.save()
        return instance


class VaccinationSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination_Site
        fields = [
            "site_address",
            "barangay",
            "city"
        ]

    def update(self, instance, validated_data):
        if validated_data.get("site_address") != "None" or validated_data.get("site_address") != "":
            instance.site_address = validated_data.get(
                "site_address", instance.site_address)
        if validated_data.get("barangay") != "None" or validated_data.get("barangay") != "":
            instance.barangay = validated_data.get(
                "barangay", instance.barangay)
        if validated_data.get("city") != "None" or validated_data.get("city") != "":
            instance.city = validated_data.get("city", instance.city)
        instance.save()
        return instance


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
            "second_vaccination_status",
            "second_vaccination_date",
            "second_vaccination_time",
            "second_vaccination_site",
            "second_vaccination_serial",
        ]

    def update(self, instance, validated_data):
        if validated_data.get("first_vaccination_status") != "None" or validated_data.get("first_vaccination_status") != "":
            instance.first_vaccination_status = validated_data.get(
                "first_vaccination_status", instance.first_vaccination_status)
        if validated_data.get("first_vaccination_date") != "None" or validated_data.get("first_vaccination_date") != "":
            instance.first_vaccination_date = validated_data.get(
                "first_vaccination_date", instance.first_vaccination_date)
        if validated_data.get("first_vaccination_time") != "None" or validated_data.get("first_vaccination_time") != "":
            instance.first_vaccination_time = validated_data.get(
                "first_vaccination_time", instance.first_vaccination_time)
        if validated_data.get("first_vaccination_site") != "None" or validated_data.get("first_vaccination_site") != "":
            instance.first_vaccination_site = validated_data.get(
                "first_vaccination_site", instance.first_vaccination_site)
        if validated_data.get("first_vaccination_serial") != "None" or validated_data.get("first_vaccination_serial") != "":
            instance.first_vaccination_serial = validated_data.get(
                "first_vaccination_serial", instance.first_vaccination_serial)
        if validated_data.get("second_vaccination_status") != "None" or validated_data.get("second_vaccination_status") != "":
            instance.second_vaccination_status = validated_data.get(
                "second_vaccination_status", instance.second_vaccination_status)
        if validated_data.get("second_vaccination_date") != "None" or validated_data.get("second_vaccination_date") != "":
            instance.second_vaccination_date = validated_data.get(
                "second_vaccination_date", instance.second_vaccination_date)
        if validated_data.get("second_vaccination_time") != "None" or validated_data.get("second_vaccination_time") != "":
            instance.second_vaccination_time = validated_data.get(
                "second_vaccination_time", instance.second_vaccination_time)
        if validated_data.get("second_vaccination_site") != "None" or validated_data.get("second_vaccination_site") != "":
            instance.second_vaccination_site = validated_data.get(
                "second_vaccination_site", instance.second_vaccination_site)
        if validated_data.get("second_vaccination_serial") != "None" or validated_data.get("second_vaccination_serial") != "":
            instance.second_vaccination_serial = validated_data.get(
                "second_vaccination_serial", instance.second_vaccination_serial)
        instance.save()
        return instance
