from django.db import models
from django.db.models.base import Model


class Eligibility_Status(models.Model):
    id = models.BigIntegerField(primary_key=True)
    status = models.CharField(max_length=15)

    class Meta:
        db_table = "eligibility_status"

    def __str__(self) -> str:
        return str(self.id)


class Medical_History(models.Model):
    pass


class Vaccination_Site(models.Model):
    vs_id = models.BigIntegerField(primary_key=True)
    site_address = models.CharField(max_length=2000, null=False)
    barangay = models.CharField(max_length=500, null=False)
    city = models.CharField(max_length=500, null=False)

    class Meta:
        db_table = "vaccination_site"


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
