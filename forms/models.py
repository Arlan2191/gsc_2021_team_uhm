from django.db import models


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
