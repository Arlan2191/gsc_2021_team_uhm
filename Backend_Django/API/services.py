from collections import OrderedDict
from API.serializers import LoginSerializer, RegistrationSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.crypto import get_random_string
from projectBakuna.environment import datastoreConfig, TABLES, SERIALIZERS
from typing import Any
from projectBakuna.exceptions import IncorrectPINException, SubscriptionException
from google.oauth2 import service_account
from google.cloud import datastore
from google.cloud.datastore.key import Key
from datetime import datetime
from threading import Thread
import time
import re


class CreateService:
    def handle(response: dict, data: dict):
        auth_token, amount_entry = CreateService.__addEntry(
            data.get("mobile_number"))
        if auth_token is not None and amount_entry is not None:
            if auth_token != "Unsubscribed":
                serializer = SERIALIZERS["PI"](data=data)
                if serializer.is_valid(raise_exception=True):
                    uID = serializer.create(serializer.validated_data).id
                    rID, PIN = CreateService.__registerUser(
                        uID, serializer.validated_data)
                    Thread(target=CreateService.__saveEntity,
                           args=[uID, response]).start()
                    Thread(target=CreateService.__saveStatus,
                           args=[uID, serializer.validated_data]).start()
                    return rID, PIN
        raise SubscriptionException

    def __addEntry(mobile_number: str):
        data = {"mobile_number": mobile_number, "auth_token": "None"}
        instance = TABLES["AM"].objects.get(
            pk=int(str(mobile_number).replace("+", "")))
        serializer = SERIALIZERS["AM"](data=data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.update(instance, serializer.validated_data)
            return instance.auth_token, instance.amount_entry

    def __saveEntity(id: int, response: dict):
        time.sleep(0.01)
        service = DatastoreService()
        service.postResponse(id, response)

    def __saveStatus(id: int, data: dict):
        time.sleep(0.01)
        _ = EligibilityService.initialize(id, data)

    def __registerUser(id: int, validated_data):
        data = {"id": id, "first_name": validated_data.get("first_name"), "last_name": validated_data.get(
            "last_name"), "mobile_number": validated_data.get("mobile_number"), "email": validated_data.get("email"), "password": get_random_string(length=8)}  # TODO
        u = AuthUserService.register(100, data)
        return u.username, data["password"]


class CreatePersonnelService:
    def handle(data: dict):
        serializer = SERIALIZERS["PRI"](data=data)
        if serializer.is_valid(raise_exception=True):
            u = serializer.create(serializer.validated_data)
            username, PIN = CreatePersonnelService.__registerUser(
                u.pk, serializer.validated_data)
            Thread(target=CreatePersonnelService.__initializeDropbox,
                   args=[u.pk, serializer.validated_data]).start()
            return username, PIN

    def __registerUser(id, validated_data):
        data = {"id": id, "username": validated_data.get("license_number"), "first_name": validated_data.get("first_name"), "last_name": validated_data.get(
            "last_name"), "mobile_number": validated_data.get("mobile_number"), "email": validated_data.get("email"), "password": get_random_string(length=8)}
        u = AuthUserService.register(10, data)
        return u.username, data["password"]

    def __initializeDropbox(id, validated_data):
        time.sleep(0.01)
        data = {"id": id, "region": validated_data.get("organization_region"), "province": validated_data.get("organization_province"), "municipality": validated_data.get("organization_municipality"), "pending_applications": 0,
                "reviewing_applications": 0, "reviewed_applications": 0}
        _ = DropboxService.initialize(data)


class AuthUserService:
    def register(type: int, user: dict):
        if type == 100:
            instance = TABLES["PI"].objects.get(pk=user.get('id'))
        elif type == 10:
            instance = TABLES["PRI"].objects.get(pk=user.get('id'))
        if instance is not None:
            serializer = RegistrationSerializer(
                data=user, partial=True) if type == 100 else RegistrationSerializer(data=user)
            if serializer.is_valid(raise_exception=True):
                return serializer.create(type, serializer.validated_data)

    def login(user: dict):
        serializer = LoginSerializer(data=user, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def change_password(old_password: str, new_password: str):  # TODO
        pass


class DatastoreService:
    datastoreCredential = service_account.Credentials.from_service_account_info(
        datastoreConfig)
    datastoreClient = datastore.Client(credentials=datastoreCredential)

    def getResponse(self, id: int):
        query = dict(self.datastoreClient.get(
            Key('Records', id, project='project-bakuna')))
        response = dict(query["Response"])
        return {"Datetime": query["Datetime"], "Response": [{"num": k, "question": response[str(k)], "answer": response[str(k)]} for k in sorted([int(a) for a in list(response.keys())])]}

    def postResponse(self, id, response):
        eKey = self.datastoreClient.key('Records', int(id))
        task = datastore.Entity(key=eKey)
        task["Response"] = {}
        if '1' in response.keys():
            task["Response"] = response
        else:
            for key in response.keys():
                if key != "personalInfo":
                    keys, vals = re.findall(
                        "[0-9]{1,2}", response[key]), re.split("\s?[0-9]{1,2}\.\s?", response[key])[1:]
                    for k, v in zip(keys, vals):
                        task["Response"][k] = v
        task["Datetime"] = str(datetime.now())
        self.datastoreClient.put(task)

    def getCities(self):
        query = list(self.datastoreClient.query(kind='Cities').fetch())
        return {"query_result": query}


class SMSService:
    def subsribe(data: dict):
        serializer = SERIALIZERS["AM"](data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                instance = TABLES["AM"].objects.get(
                    pk=int(data["mobile_number"].replace("+", "")))
                instance = serializer.update(
                    instance, serializer.validated_data)
                if instance.amount_entry != 0:
                    return True, instance.current_verify_code
                return True, None
            except ObjectDoesNotExist:
                serializer.create(serializer.validated_data)
                return True, None
        return False, None

    def verify(data: dict):
        retries = 0
        while retries < 3:
            try:
                print("RETRYING: ", retries)
                instance = TABLES["AM"].objects.get(
                    pk=int(data["mobile_number"].replace("+", "")))
                if instance is not None:
                    return True
            except ObjectDoesNotExist:
                retries += 1
                time.sleep(1)
        return False

    def getStatusObject(uID: int, mobile_number: str, rID: str, PIN: str):
        e = TABLES["PI"].objects.get(id=uID)
        if mobile_number == e.mobile_number:
            try:
                if AuthUserService.login({"username": rID, "password": PIN}) is not None:
                    instance = EligibilityService.view(uID)
                    return e.first_name, instance
            except Exception as e:
                print(e)
                raise IncorrectPINException
        raise ObjectDoesNotExist

    def unsubcribe(mobile_number: str):
        amn = TABLES["AM"].objects.get(
            pk=int(mobile_number.replace("+", "")))
        amn_serializer = SERIALIZERS["AM"](
            data={"mobile_number": mobile_number, "auth_token": "Unsubscribed"})
        if amn_serializer.is_valid(raise_exception=True):
            amn_serializer.update(amn, amn_serializer.validated_data)
            return True
        return False


class DropboxService:
    def initialize(data: dict):
        serializer = SERIALIZERS["EA"](data=data)
        if serializer.is_valid(raise_exception=True):
            _ = serializer.create(serializer.validated_data)

    def view(id: int):
        instance = TABLES["EA"].objects.get(pk=id)
        return SERIALIZERS["EA"](instance).data

    def update(id: int, data: dict):
        time.sleep(0.01)
        instance = TABLES["EA"].objects.get(pk=id)
        serializer = SERIALIZERS["EA"](data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            _ = serializer.update(instance, serializer.validated_data)


class EligibilityService:

    def initialize(id: int, validated_data: dict):
        try:
            personnel = TABLES["EA"].objects.raw(
                "SELECT id_id FROM eligibility_applications WHERE pending_applications=(SELECT MIN(pending_applications) FROM eligibility_applications) AND region='{}' AND province='{}' AND municipality='{}' LIMIT 1".format(validated_data.get("region"), validated_data.get("province"), validated_data.get("municipality")))[0]
            data = {"id": id, "status": "P", "assigned_to": personnel.id_id,
                    "reason": "Assigned medical personnel has yet to review your application"}
            serializer = SERIALIZERS["ES"](data=data)
            if serializer.is_valid(raise_exception=True):
                instance = serializer.create(serializer.validated_data)
                Thread(target=DropboxService.update, args=[personnel.id_id, {
                    "pending_applications": personnel.pending_applications + 1}]).start()
        except IndexError:
            pass  # TODO

    def view(id: int):
        instance = TABLES["ES"].objects.get(pk=id)
        return instance

    def update(id: int, data: dict):
        print(data)
        instance = TABLES["ES"].objects.get(pk=id)
        serializer = SERIALIZERS["ES"](data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.update(instance, serializer.validated_data)
            if data.get("status") == "G" or data.get("status") == "G@R":
                Thread(target=TrackingService.create, args=[id]).start()
            return instance.pk


class TrackingService:
    def create(uID: str):
        time.sleep(0.01)
        s1 = SERIALIZERS["TI"](
            data={'user': uID, 'dose': '1st'})
        if s1.is_valid():
            s1.create(validated_data=s1.validated_data)
        s2 = SERIALIZERS["TI"](
            data={'user': uID, 'dose': '2nd'})
        if s2.is_valid():
            s2.create(validated_data=s2.validated_data)

    def update(uID: str, dose: str, data: dict):
        u = TABLES["TI"].objects.get(user=uID, dose=dose)
        s = SERIALIZERS["TI"](u, data=data, partial=True)
        if s.is_valid(raise_exception=True):
            s.update(u, validated_data=s.validated_data)


class NotificationService:  # TODO
    def get(ordered: bool, filters):
        recipients = []
        if not ordered:
            priority = filters.get("priority", None)
            birth_range = filters.get("birth_range", None)
            max_cap = filters.get("max_cap", None)
            barangay = filters.get("barangay", None)
            if max_cap is not None:
                if priority is not None:
                    if barangay is not None:
                        if birth_range is not None:
                            if isinstance(priority, (list, tuple)):
                                for p in priority:
                                    if isinstance(barangay, (list, tuple)):
                                        for b in barangay:
                                            recipients += [SERIALIZERS["PI"](x).data.get("mobile_number") for x in TABLES["PI"].objects.filter(
                                                priority=p, barangay=b, birthdate_range=birth_range)]
                                    else:
                                        recipients += [SERIALIZERS["PI"](x).data.get("mobile_number") for x in TABLES["PI"].objects.filter(
                                            priority=p, barangay=barangay, birthdate_range=birth_range)]
                            else:
                                recipients += [SERIALIZERS["PI"](x).data.get("mobile_number") for x in TABLES["PI"].objects.filter(
                                    priority=priority, barangay=barangay, birthdate_range=birth_range)]
                        else:
                            if isinstance(priority, (list, tuple)):
                                for p in priority:
                                    if isinstance(barangay, (list, tuple)):
                                        for b in barangay:
                                            recipients += [SERIALIZERS["PI"](x).data.get(
                                                "mobile_number") for x in TABLES["PI"].objects.filter(priority=p, barangay=b)]
                                    else:
                                        recipients += [SERIALIZERS["PI"](x).data.get(
                                            "mobile_number") for x in TABLES["PI"].objects.filter(priority=p, barangay=barangay)]
                            else:
                                recipients += [SERIALIZERS["PI"](x).data.get(
                                    "mobile_number") for x in TABLES["PI"].objects.filter(priority=priority, barangay=barangay)]
                    elif birth_range is not None:
                        if isinstance(priority, (list, tuple)):
                            for p in priority:
                                recipients += [SERIALIZERS["PI"](x).data.get(
                                    "mobile_number") for x in TABLES["PI"].objects.filter(priority=p, birthdate_range=birth_range)]
                        else:
                            recipients += [SERIALIZERS["PI"](x).data.get("mobile_number") for x in TABLES["PI"].objects.filter(
                                priority=priority, birthdate_range=birth_range)]
                    else:
                        if isinstance(priority, (list, tuple)):
                            for p in priority:
                                recipients += [SERIALIZERS["PI"](x).data.get(
                                    "mobile_number") for x in TABLES["PI"].objects.filter(priority=p)]
                        else:
                            recipients += [SERIALIZERS["PI"](x).data.get(
                                "mobile_number") for x in TABLES["PI"].objects.filter(priority=priority)]
                elif barangay is not None:
                    if birth_range is not None:
                        pass
                    else:
                        pass
                elif birth_range is not None:
                    pass
                else:
                    pass
            else:
                raise ValueError(
                    "Maximum number of recipients must be defined")
        else:
            pass

    def send():
        pass
