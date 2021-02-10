from django.db import models
from rest_framework import status


class Personal_Information(models.Model):
    first_name = models.CharField(max_length=2000)
    middle_name = models.CharField(max_length=2000)
    last_name = models.CharField(max_length=2000)
    birthdate = models.DateField()
    sex = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=15)
    home_address = models.CharField(max_length=2000)
    city = models.CharField(max_length=2000)
    barangay = models.CharField(max_length=2000)

    class Meta:
        db_table = "personal_information"

    def __str__(self) -> str:
        return self.first_name


class Auth_Mobile_Number(models.Model):
    mobile_number = models.CharField(max_length=15)
    amount_entry = models.SmallIntegerField()

    class Meta:
        db_table = "auth_mobile_number"

    def __str__(self) -> str:
        return self.mobile_number


class Eligibility_Status(models.Model):
    id = models.BigIntegerField(primary_key=True)
    status = models.CharField(max_length=15)

    class Meta:
        db_table = "eligibility_status"

    def __str__(self) -> str:
        return str(self.id)


class Tracking_Information(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_vaccination_status = models.CharField(max_length=15)
    first_vaccination_date = models.DateField()
    first_vaccination_time = models.TimeField()
    first_vaccination_site = models.IntegerField()
    first_vaccination_serial = models.CharField(max_length=1000)
    second_vaccination_status = models.CharField(max_length=15)
    second_vaccination_date = models.DateField()
    second_vaccination_time = models.TimeField()
    second_vaccination_site = models.IntegerField()
    second_vaccination_serial = models.CharField(max_length=1000)

    class Meta:
        db_table = "tracking_information"

    def __str__(self) -> str:
        return str(self.id)
