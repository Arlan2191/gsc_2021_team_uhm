from django.core.validators import validate_comma_separated_integer_list
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import jwt
from sqlalchemy.sql.expression import true


class Local_Government_Units(models.Model):
    lgu_id = models.BigAutoField(primary_key=True)
    region = models.TextField(null=False)
    province = models.TextField(null=False)
    municipality = models.TextField(null=False)

    class Meta:
        db_table = "local_government_units"


class Local_Government_Unit_Admin(models.Model):
    lgu_id = models.OneToOneField(
        Local_Government_Units, primary_key=True, on_delete=models.RESTRICT)
    organization = models.CharField(max_length=200, null=False)
    organization_email = models.EmailField(null=False)
    organization_telecom = models.TextField(null=False)
    organization_region = models.TextField(null=False)
    organization_province = models.TextField(null=False)
    organization_municipality = models.TextField(null=False)

    class Meta:
        db_table = "local_government_unit_admin"


class Vaccination_Site(models.Model):
    site_id = models.BigAutoField(primary_key=True)
    lgu_id = models.ForeignKey(
        Local_Government_Units, blank=False, null=False, on_delete=models.RESTRICT)
    barangay = models.TextField(null=False)
    site_address = models.TextField(null=False)

    class Meta:
        db_table = "vaccination_site"


class Vaccination_Priority(models.IntegerChoices):
    UNASSIGNED = 0, _('unassigned')
    MEDICAL_FRONTLINER = 1, _('medical_frontliner')
    INDIGENT_SENIOR_CITIZEN = 2, _('indigent_senior_citizen')
    SENIOR_CITIZEN = 3, _('senior_citizen')
    INDIGENT_POPULATION = 4, _('indigent_population')
    UNIFORMED_PERSONNEL = 5, _('uniformed_personnel')
    SCHOOL_TEACHERS_AND_HEALTH_WORKERS = 6, _(
        'school_teachers_and_health_workers')
    GOVERNMENT_WORKER = 7, _('government_worker')
    ESSENTIAL_WORKER = 8, _('essential_worker')
    AT_RISK_SOCIODEMOGRAPHIC_GROUP = 9, _('at_risk_sociodemographic_group')
    OFW = 10, _('overseas_filipino_worker')
    REMAINING_WORKFORCE = 11, _('remaining_workforce')
    STUDENTS = 12, _('student')


class Eligibility_Labels(models.TextChoices):
    GRANTED = 'G', _('granted')
    GRANTED_RISK = 'G@R', _('granted@risk')
    DENIED = 'D', _('denied')
    PENDING = 'P', _('pending')


class Dose_Labels(models.TextChoices):
    FIRST = '1st', _('first')
    SECOND = '2nd', _('second')


class Tracking_Labels(models.TextChoices):
    COMPLETE = 'C', _('complete')
    INELIGIBLE = 'I', _('ineligible')
    WAITING = 'W', _('waiting')
    PENDING = 'P', _('pending')
    MISSED = 'M', _('missed')


class Vaccination_Session(models.Model):
    lgu_id = models.ForeignKey(
        Local_Government_Units, blank=False, null=False, on_delete=models.RESTRICT)
    vs_id = models.BigAutoField(primary_key=True)
    site = models.ForeignKey(
        Vaccination_Site, on_delete=models.RESTRICT)
    amount_confirm = models.BigIntegerField(default=0, null=False)
    dose = models.CharField(
        max_length=3, choices=Dose_Labels.choices, default=Dose_Labels.FIRST)
    date = models.DateField(blank=True)
    time = models.CharField(max_length=10, blank=True)
    max_cap = models.BigIntegerField(blank=True, null=False)
    target_barangay = models.TextField(blank=True, null=True)
    birth_range = models.TextField(blank=True, null=True)
    priority = models.TextField(
        validators=[validate_comma_separated_integer_list])

    class Meta:
        db_table = "vaccination_sessions"


class Sex(models.TextChoices):
    MALE = 'M', _('male')
    FEMALE = 'F', _('female')


class Personal_Information(models.Model):
    id = models.BigAutoField(primary_key=True)
    lgu_id = models.ForeignKey(
        Local_Government_Units, blank=False, null=False, on_delete=models.RESTRICT)
    first_name = models.CharField(max_length=200, null=False)
    middle_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    birthdate = models.DateField(null=False)
    sex = models.CharField(max_length=1, choices=Sex.choices, null=False)
    occupation = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, null=False)
    region = models.TextField(null=False)
    province = models.TextField(null=False)
    municipality = models.TextField(null=False)
    barangay = models.TextField(null=False)
    home_address = models.CharField(max_length=1000)

    class Meta:
        db_table = "personal_information"

    def __str__(self) -> str:
        return self.first_name


class Auth_Mobile_Number(models.Model):
    mn_id = models.BigIntegerField(primary_key=True)
    mobile_number = models.CharField(max_length=15, null=False)
    auth_token = models.CharField(max_length=50, null=False)
    amount_entry = models.SmallIntegerField(default=0, null=False)
    current_verify_code = models.CharField(
        max_length=4, blank=True, null=True, default=None)

    class Meta:
        db_table = "auth_mobile_number"

    def __str__(self) -> str:
        return self.mobile_number


class AuthUserManager(BaseUserManager):

    def create_user(self, id, lgu_id, username, mobile_number, first_name, last_name, email=None, password=None):
        if id is None:
            raise TypeError('Users must have a reference ID')
        if username is None:
            raise TypeError('Users must have a username')
        if mobile_number is None:
            raise TypeError('Users must have a mobile number')
        user = self.model(id=id, lgu_id=lgu_id, username=username, mobile_number=mobile_number,
                          first_name=first_name, last_name=last_name, email=self.normalize_email(email))
        user.set_password(password)
        user.user_permissions.set([6, 8, 16, 20, 24, 32])
        user.save()
        return user

    def create_staffuser(self, id, lgu_id, username, mobile_number, first_name, last_name, password, email=None):
        if id is None:
            raise TypeError('Staff must have a reference ID')
        if username is None:
            raise TypeError('Staff must have a username')
        if username is None:
            raise TypeError('Staff must have a password')
        if mobile_number is None:
            raise TypeError('Staff must have a mobile number')
        user = self.create_user(id=id, lgu_id=lgu_id, username=username, mobile_number=mobile_number,
                                first_name=first_name, last_name=last_name, email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = True
        user.user_permissions.set(
            [8, 10, 12, 13, 14, 15, 16, 18, 20, 21, 22, 23, 24, 30, 32])
        user.save()
        return user

    def create_adminuser(self, id, lgu_id, username, mobile_number, first_name, last_name, password, email=None):
        if id is None:
            raise TypeError('Admin must have a reference ID')
        if username is None:
            raise TypeError('Admin must have a username')
        if username is None:
            raise TypeError('Admin must have a password')
        if mobile_number is None:
            raise TypeError('Admin must have a mobile number')
        user = self.create_user(id=id, lgu_id=lgu_id, username=username, mobile_number=mobile_number,
                                first_name=first_name, last_name=last_name, email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.user_permissions.set(
            [8, 10, 12, 13, 14, 15, 16, 18, 20, 21, 22, 23, 24, 30, 32])
        user.save()
        return user

    def create_superuser(self, username, mobile_number, first_name, last_name, password, email=None):
        if mobile_number is None:
            raise TypeError('Superusers must have a mobile number')
        if password is None:
            raise TypeError('Superusers must have a password')
        user = self.create_user(id=1, username=username, mobile_number=mobile_number,
                                first_name=first_name, last_name=last_name, email=self.normalize_email(email))
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class AuthUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigIntegerField(null=False)
    lgu_id = models.ForeignKey(
        Local_Government_Units, blank=True, default=None, null=False, on_delete=models.RESTRICT)
    password = models.CharField(max_length=128, null=False)
    last_login = models.DateTimeField(max_length=6, blank=True, null=True)
    username = models.CharField(primary_key=True, max_length=150, null=False)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(blank=True, null=True, max_length=100)
    mobile_number = models.CharField(null=False, max_length=15)
    date_created = models.DateTimeField(auto_now=True, null=False)
    date_updated = models.DateTimeField(auto_now=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_admin = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['id', 'lgu_id',
                       'first_name', 'last_name', 'mobile_number']

    objects = AuthUserManager()

    @property
    def token(self):
        return self.__generate_jwt_token()

    def get_full_name(self):
        return ", ".join([self.last_name, self.first_name])

    def get_short_name(self):
        return self.first_name

    def __generate_jwt_token(self):
        dt = datetime.now() + timedelta(1)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    class Meta:
        db_table = "auth_user"
        unique_together = ["id", "is_staff", "username"]

    def __str__(self) -> str:
        return str(self.username)


class Personnel_Information(models.Model):
    id = models.BigAutoField(primary_key=True)
    lgu_id = models.ForeignKey(
        Local_Government_Units, blank=False, null=False, on_delete=models.RESTRICT)
    license_number = models.CharField(max_length=200, unique=True, null=False)
    first_name = models.CharField(max_length=200, null=False)
    middle_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    birthdate = models.DateField(null=False)
    sex = models.CharField(max_length=1, choices=Sex.choices, null=False)
    occupation = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, null=False)
    organization = models.CharField(max_length=200, null=False)
    organization_email = models.EmailField(null=False)
    organization_telecom = models.TextField(null=False)
    organization_region = models.TextField(null=False)
    organization_province = models.TextField(null=False)
    organization_municipality = models.TextField(null=False)
    organization_barangay = models.TextField(null=False)
    organization_address = models.TextField(null=False)

    class Meta:
        db_table = "personnel_information"

    def __str__(self) -> str:
        return str(self.id)


class Eligibility_Status(models.Model):
    id = models.OneToOneField(Personal_Information,
                              primary_key=True, on_delete=models.RESTRICT)
    lgu_id = models.ForeignKey(
        Local_Government_Units, blank=False, null=False, on_delete=models.RESTRICT)
    assigned_to = models.ForeignKey(
        Personnel_Information, null=False, on_delete=models.RESTRICT)
    priority = models.SmallIntegerField(
        choices=Vaccination_Priority.choices, default=Vaccination_Priority.UNASSIGNED)
    status = models.CharField(
        max_length=3, choices=Eligibility_Labels.choices, default=Eligibility_Labels.PENDING)
    reason = models.CharField(max_length=4000)

    class Meta:
        db_table = "eligibility_status"

    def __str__(self) -> str:
        return str(self.id)


class Eligibility_Applications(models.Model):
    id = models.OneToOneField(Personnel_Information,
                              primary_key=True, on_delete=models.RESTRICT)
    lgu_id = models.ForeignKey(
        Local_Government_Units, blank=False, null=False, on_delete=models.RESTRICT)
    pending_applications = models.PositiveBigIntegerField(default=0)
    reviewing_application = models.ForeignKey(
        Eligibility_Status, null=True, on_delete=models.RESTRICT)
    reviewed_applications = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = "eligibility_applications"
        ordering = ["pending_applications"]


class Tracking_Information(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        Personal_Information, on_delete=models.RESTRICT, blank=True, null=True)
    notified = models.BooleanField(default=False, null=False)
    confirmed = models.BooleanField(default=False, null=False)
    dose = models.CharField(
        max_length=3, choices=Dose_Labels.choices, default=Dose_Labels.FIRST)
    status = models.CharField(
        max_length=2, choices=Tracking_Labels.choices, default=Tracking_Labels.PENDING)
    batch_number = models.IntegerField(blank=True, null=True)
    session = models.ForeignKey(
        Vaccination_Session, on_delete=models.RESTRICT, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    site = models.ForeignKey(
        Vaccination_Site, on_delete=models.RESTRICT, blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    license_number = models.ForeignKey(
        Personnel_Information, on_delete=models.RESTRICT, blank=True, null=True)
    serial = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "tracking_information"
        unique_together = ["user", "dose"]

    def __str__(self) -> str:
        return str(self.user)
