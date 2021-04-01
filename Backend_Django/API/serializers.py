from collections import OrderedDict
import random
from rest_framework import serializers
from projectBakuna.exceptions import MaxEntryException, InvalidNumber, InvalidUserType
from API.models import Auth_Mobile_Number, Eligibility_Applications, Personnel_Information, Personal_Information, Eligibility_Status, Tracking_Information, Vaccination_Priority, Vaccination_Site, AuthUser, Vaccination_Session
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = AuthUser
        fields = ('id', 'username', 'password', 'token',
                  'first_name', 'last_name', 'mobile_number')

    def create(self, type, validated_data):
        if type is None:
            raise TypeError('Register data must include user type')
        if type == 100:
            validated_data['username'] = "{}-{}-{}".format(
                '00', '0000', validated_data.get('id'))
            return AuthUser.objects.create_user(**validated_data)
        if type == 10:
            return AuthUser.objects.create_staffuser(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = AuthUser
        fields = ['username', 'password', 'token', 'id']

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError(
                'A username is required to log in'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated'
            )
        return {
            'username': user.username,
            'id': user.id,
            'token': user.token,
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = (
            "username",
            "email",
            "password",
            "token",
        )
        read_only_fields = ('token', 'username')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            if value != None:
                setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal_Information
        fields = [
            "priority",
            "first_name",
            "middle_name",
            "last_name",
            "birthdate",
            "sex",
            "occupation",
            "email",
            "mobile_number",
            "region",
            "province",
            "municipality",
            "barangay",
            "home_address"
        ]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if value != None:
                setattr(instance, key, value)
        instance.save()
        return instance


class PersonnelInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnel_Information
        fields = [
            "license_number",
            "first_name",
            "middle_name",
            "last_name",
            "birthdate",
            "sex",
            "occupation",
            "email",
            "mobile_number",
            "organization",
            "organization_email",
            "organization_telecom",
            "organization_region",
            "organization_province",
            "organization_municipality",
            "organization_barangay",
            "organization_address"
        ]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if value != None and key != "license_number":
                setattr(instance, key, value)
        instance.save()
        return instance


class AuthMobileNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth_Mobile_Number
        fields = [
            "mobile_number",
            "auth_token",
        ]

    def create(self, validated_data):
        try:
            mn = int(str(validated_data.get("mobile_number")).replace("+", ""))
            validated_data = OrderedDict([('mn_id', mn), ('mobile_number', validated_data.get(
                "mobile_number")), ('auth_token', validated_data.get("auth_token")), ('amount_entry', 0)])
            return Auth_Mobile_Number.objects.create(**validated_data)
        except ValueError:
            raise InvalidNumber
        except Exception as e:
            raise e

    def update(self, instance, validated_data):
        if instance.amount_entry <= 9 and validated_data.get("auth_token") == "None":
            instance.current_verify_code = None
            instance.amount_entry += 1
        elif validated_data.get("auth_token") == "None":
            instance.current_verify_code = None
            raise MaxEntryException
        if validated_data.get("auth_token") != "None" and validated_data.get("auth_token") != "":
            instance.current_verify_code = "".join(
                [str(random.randint(0, 9)) for _ in range(4)])
            instance.auth_token = validated_data.get(
                "auth_token", instance.auth_token)
        instance.save()
        return instance


class EligibilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eligibility_Status
        fields = [
            "id",
            "assigned_to",
            "priority",
            "status",
            "reason",
        ]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if value != None:
                setattr(instance, key, value)
        instance.save()
        return instance


class EligibilityApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eligibility_Applications
        fields = [
            "id",
            "region",
            "province",
            "municipality",
            "pending_applications",
            "reviewing_applications",
            "reviewed_applications"
        ]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if value != None:
                setattr(instance, key, value)
        instance.save()
        return instance


class VaccinationSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination_Site
        fields = [
            "site_id",
            "region",
            "province",
            "municipality",
            "barangay",
            "site_address",
        ]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if value != None:
                setattr(instance, key, value)
        instance.save()
        return instance


class VaccinationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination_Session
        fields = [
            "vs_id",
            "site",
            "date",
            "time",
            "max_cap",
            "target_barangay",
            "birth_range",
            "priority",
        ]

    def create(self, validated_data):
        choices = validated_data.get("priority", None)
        if choices is not None:
            for c in choices.split(","):
                if int(c) <= 0 or int(c) >= 13:
                    raise TypeError("Priority list items must be [1, 12]")
        else:
            raise TypeError("Priority list is required")
        return Vaccination_Session.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if value != None:
                setattr(instance, key, value)
        instance.save()
        return instance


class TrackingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking_Information
        fields = [
            "user",
            "dose",
            "status",
            "batch_number",
            "session",
            "time",
            "site",
            "manufacturer",
            "license_number",
            "serial",
        ]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if value != None and key != "user" and key != "dose":
                setattr(instance, key, value)
        instance.save()
        return instance
