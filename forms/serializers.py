from collections import OrderedDict
from rest_framework import serializers
from FORMS.models import Auth_Mobile_Number, Personal_Information


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

    def update(self, instance, validated_data):
        if validated_data.get("first_name") != "None" or validated_data.get("first_name") != "":
            instance.first_name = validated_data.get(
                "first_name", instance.first_name)
        if validated_data.get("middle_name") != "None" or validated_data.get("middle_name") != "":
            instance.middle_name = validated_data.get(
                "middle_name", instance.middle_name)
        if validated_data.get("last_name") != "None" or validated_data.get("last_name") != "":
            instance.last_name = validated_data.get(
                "last_name", instance.last_name)
        if validated_data.get("birthdate") != "None" or validated_data.get("birthdate") != "":
            instance.birthdate = validated_data.get(
                "birthdate", instance.birthdate)
        if validated_data.get("sex") != "None" or validated_data.get("sex") != "":
            instance.sex = validated_data.get(
                "sex", instance.sex)
        if validated_data.get("mobile_number") != "None" or validated_data.get("mobile_number") != "":
            instance.mobile_number = validated_data.get(
                "mobile_number", instance.mobile_number)
        if validated_data.get("home_address") != "None" or validated_data.get("home_address") != "":
            instance.home_address = validated_data.get(
                "home_address", instance.home_address)
        if validated_data.get("city") != "None" or validated_data.get("city") != "":
            instance.city = validated_data.get("city", instance.city)
        if validated_data.get("barangay") != "None" or validated_data.get("barangay") != "":
            instance.barangay = validated_data.get(
                "barangay", instance.barangay)
        instance.save()
        return instance


class AuthMobileNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth_Mobile_Number
        fields = [
            "mobile_number",
            "auth_token"
        ]

    def create(self, validated_data):
        try:
            mn = int(str(validated_data.get("mobile_number")).replace("+", ""))
            try:
                existingQuery = Auth_Mobile_Number.objects.get(pk=mn)
                if existingQuery.amount_entry <= 9:
                    validated_data = OrderedDict(
                        [('amount_entry', existingQuery.amount_entry + 1), ('auth_token', validated_data.get("auth_token"))])
                    return self.update(existingQuery, validated_data)
                raise MaxEntryException
            except Auth_Mobile_Number.DoesNotExist:
                validated_data = OrderedDict([('mn_id', mn), ('mobile_number', validated_data.get(
                    "mobile_number")), ('auth_token', validated_data.get("auth_token")), ('amount_entry', 1)])
                return Auth_Mobile_Number.objects.create(**validated_data)
            except Exception as e:
                raise e
        except Exception as e:
            raise InvalidNumber

    def update(self, instance, validated_data):
        if validated_data.get("mobile_number") != "None" or validated_data.get("mobile_number") != "":
            instance.mobile_number = validated_data.get(
                "mobile_number", instance.mobile_number)
        if validated_data.get("auth_token") != "None" or validated_data.get("auth_token") != "":
            instance.auth_token = validated_data.get(
                "auth_token", instance.auth_token)
        instance.save()
        return instance


class MaxEntryException(Exception):
    def __str__(self) -> str:
        return "Maximum entries for this mobile number attained. We will not receive anymore entries from this number."


class InvalidNumber(Exception):
    def __str__(self) -> str:
        return "Invalid Mobile Number"
