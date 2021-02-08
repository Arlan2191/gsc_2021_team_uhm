from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MobilePhone
import base64

EXPIRY_TIME = 60 # seconds


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now()))


class PhoneNumberAuthentication(APIView):
    """
        Basic OTP based from https://github.com/Akash16s/OTP-in-django
    """

    # Returns an OTP key
    @staticmethod
    def get(request, phone):
        try:
            # Check if number already exists
            Number = MobilePhone.objects.get(Number=phone)
        except ObjectDoesNotExist:
            # Create new mobile phone object
            MobilePhone.objects.create(
                Number=phone,
            )
            Number = phoneModel.objects.get(Number=phone)

        Number.save()

        # Generate key
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())

        # Time base otp
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)

        return Response({"otp-key": OTP.now()}, status=200)

    # Verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Number = MobilePhone.objects.get(Number=phone)
        except ObjectDoesNotExist:
            return Response("Number does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model
        if OTP.verify(request.data["otp-key"]):  # Verifying the OTP
            Number.isVerified = True
            Number.save()
            return Response("valid OTP", status=200)
        return Response("wrong/expired OTP", status=400)
