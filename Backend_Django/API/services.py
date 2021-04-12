from SMS.library import defaultResponse
from API.models import Eligibility_Status, Tracking_Information
from requests import post
from collections import OrderedDict
from functools import partial
from API.serializers import LGUAdminSerializer, LoginSerializer, RegistrationSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.crypto import get_random_string
from projectBakuna.environment import datastoreConfig, TABLES, SERIALIZERS, ENGINE, globeConfig
from typing import Any
from projectBakuna.exceptions import ConfirmationException, IncorrectPINException, SubscriptionException
from google.oauth2 import service_account
from google.cloud import datastore
from google.cloud.datastore.key import Key
from datetime import datetime
from threading import Thread
from aldjemy import core
from sqlalchemy.sql import text
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
        data = {"id": id, "lgu_id": validated_data.get("lgu_id").lgu_id, "first_name": validated_data.get("first_name"), "last_name": validated_data.get(
            "last_name"), "mobile_number": validated_data.get("mobile_number"), "email": validated_data.get("email"), "password": get_random_string(length=8)}  # TODO
        u = AuthUserService.register(100, data)
        return u.username, data["password"]


class CreatePersonnelService:
    def handle(data: dict):
        serializer = SERIALIZERS["PRI"](data=data)
        if serializer.is_valid(raise_exception=True):
            u = serializer.create(serializer.validated_data)
            username, PIN = CreatePersonnelService.__registerUser(
                u.pk, 10, serializer.validated_data)
            Thread(target=CreatePersonnelService.__initializeDropbox,
                   args=[u.pk, serializer.validated_data]).start()
            return username, PIN

    def __registerUser(id, type, validated_data):
        if type == 10:
            data = {"id": id, "lgu_id": validated_data.get("lgu_id").lgu_id, "username": validated_data.get("license_number"), "first_name": validated_data.get("first_name"), "last_name": validated_data.get(
                "last_name"), "mobile_number": validated_data.get("mobile_number"), "email": validated_data.get("email"), "password": get_random_string(length=8)}
        elif type == 1:
            data = {"id": id, "lgu_id": validated_data.get("lgu_id").lgu_id, "username": validated_data.get("organization"), "first_name": validated_data.get("organization"), "last_name": validated_data.get(
                "organization"), "mobile_number": validated_data.get("organization_telecom"), "email": validated_data.get("organization_email"), "password": get_random_string(length=8)}
        u = AuthUserService.register(type, data)
        return u.pk, data["password"]

    def __initializeDropbox(id, validated_data):
        time.sleep(0.01)
        data = {"id": id, "lgu_id": validated_data.get(
            "lgu_id").lgu_id, "pending_applications": 0, "reviewed_applications": 0}
        _ = DropboxService.initialize(data)

    def register(data: dict):
        serializer = SERIALIZERS["LGUA"](data=data)
        if serializer.is_valid(raise_exception=True):
            u = serializer.create(serializer.validated_data)
            username, PIN = CreatePersonnelService.__registerUser(
                u.pk, 1, serializer.validated_data)
            return username, PIN


class AuthUserService:
    def register(type: int, user: dict):
        if type == 100:
            instance = TABLES["PI"].objects.get(pk=user.get('id'))
        elif type == 10:
            instance = TABLES["PRI"].objects.get(pk=user.get('id'))
        elif type == 1:
            instance = TABLES["LGUA"].objects.get(pk=user.get('id'))
        if instance is not None:
            if type == 100:
                serializer = RegistrationSerializer(data=user, partial=True)
            elif type == 10 or type == 1:
                serializer = RegistrationSerializer(data=user)
            if serializer is not None:
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

    def getSessionConfirmations(self, lgu_id, id):
        task = self.datastoreClient.get(
            Key('Sessions', lgu_id, project='project-bakuna'))
        return dict(task)

    def initSessionConfirmations(self, lgu_id, id):
        time.sleep(0.01)
        eKey = self.datastoreClient.key('Sessions', int(lgu_id))
        task = datastore.Entity(key=eKey)
        task[str(id)] = []
        self.datastoreClient.put(task)

    def updateSessionConfirmations(self, lgu_id, id, uID):
        task = self.datastoreClient.get(
            Key('Sessions', int(lgu_id), project='project-bakuna'))
        print(task)
        task[str(id)].append(uID)
        self.datastoreClient.put(task)


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
        serializer = SERIALIZERS["EA"](data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            _ = serializer.create(serializer.validated_data)

    def view(id: int):
        instance = TABLES["EA"].objects.get(pk=id)
        return SERIALIZERS["EA"](instance).data

    def update(id: int, data: dict):
        time.sleep(0.01)
        print(data)
        instance = TABLES["EA"].objects.get(pk=id)
        serializer = SERIALIZERS["EA"](data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            _ = serializer.update(instance, serializer.validated_data)


class EligibilityService:

    def initialize(id: int, validated_data: dict):
        personnel = TABLES["EA"].objects.raw(
            "SELECT id_id FROM eligibility_applications WHERE pending_applications=(SELECT MIN(pending_applications) FROM eligibility_applications WHERE lgu_id_id=%(lgu_id)s) AND lgu_id_id=%(lgu_id)s LIMIT 1" % {"lgu_id": validated_data.get("lgu_id").lgu_id})[0]
        print(personnel)
        data = {"id": id, "lgu_id": validated_data.get("lgu_id").lgu_id, "status": "P", "assigned_to": personnel.id_id,
                "reason": "Assigned medical personnel has yet to review your application"}
        serializer = SERIALIZERS["ES"](data=data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.create(serializer.validated_data)
            Thread(target=DropboxService.update, args=[personnel.id_id, {
                "pending_applications": personnel.pending_applications + 1}]).start()

    def view(id: int):
        print(id)
        instance = TABLES["ES"].objects.get(pk=id)
        return instance

    def update(id: int, data: dict):
        instance = TABLES["ES"].objects.get(pk=id)
        serializer = SERIALIZERS["ES"](data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.update(instance, serializer.validated_data)
            ea_data = DropboxService.view(instance.assigned_to.pk)
            ea_data["reviewed_applications"] += 1
            if data.get("status") == "G" or data.get("status") == "G@R":
                Thread(target=TrackingService.create, args=[id]).start()
                Thread(target=EligibilityService.notify,
                       args=[id, instance]).start()
            Thread(target=DropboxService.update, args=[
                   instance.assigned_to.pk, data]).start()
            return instance.pk

    def notify(id: int, instance):
        time.sleep(0.01)
        query = text("SELECT m.mobile_number, auth_token, email, first_name FROM (personal_information AS p INNER JOIN auth_mobile_number AS m ON p.mobile_number=m.mobile_number AND (m.auth_token!='Unsubscribed' OR p.email!='N/A')) INNER JOIN eligibility_status AS e ON p.id=e.id_id WHERE (e.status='G' OR e.status='G@R') AND p.id={} LIMIT 1".format(id))
        connection = ENGINE.connect()
        recipient = connection.execute(query).fetchall()
        message = defaultResponse["defaultEligibilityNotification"].format(
            recipient[0][3], str(instance.get_status_display()).upper())
        senderAddress = globeConfig.get("shortCodeCrossTelco")[-4:]
        data = {"outboundSMSMessageRequest": {"clientCorrelator": "0000", "senderAddress": str(senderAddress),
                                              "outboundSMSTextMessage": {"message": "{}".format(message)}, "address": "tel: {}".format(str(recipient[0][0]))}}
        senderAddress = globeConfig.get("shortCode")[-4:]
        _ = post(url="https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/{}/requests?access_token={}".format(
            senderAddress, str(recipient[0][1])), json=data)


class ConfirmationService:

    def handle(uID, lgu_id):
        print(lgu_id)
        try:
            isFirst = False
            instance1 = TABLES["TI"].objects.get(user_id=uID, dose='1st')
            instance2 = TABLES["TI"].objects.get(user_id=uID, dose='2nd')
            if (instance1.status == 'P' and instance1.notified == True) and (instance2.status == 'P' and instance2.notified == False):
                session_id = instance1.session.vs_id
                TrackingService.update(uID, '1st', {"confirmed": True})
                isFirst = True
            elif instance2.status == 'P' and instance2.notified == True:
                session_id = instance2.session.vs_id
                TrackingService.update(uID, '2nd', {"confirmed": True})
            instance = TABLES["VSS"].objects.get(pk=session_id)
            if isFirst:
                TrackingService.update(
                    uID, '1st', {"site_id": instance.site_id, "date": instance.date})
            else:
                TrackingService.update(
                    uID, '2nd', {"site_id": instance.site_id, "date": instance.date})
            serializer = SERIALIZERS["VSS"](
                instance, data={"amount_confirm": instance.amount_confirm + 1}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.update(
                    instance, validated_data=serializer.validated_data)
            ds = DatastoreService()
            ds.updateSessionConfirmations(lgu_id, session_id, uID)
            return instance
        except ObjectDoesNotExist:
            raise ConfirmationException


class TrackingService:
    def create(uID: str):
        time.sleep(0.01)
        s1 = SERIALIZERS["TI"](
            data={'user': uID, 'dose': '1st', 'notified': False, 'confirmed': False})
        if s1.is_valid():
            s1.create(validated_data=s1.validated_data)
        s2 = SERIALIZERS["TI"](
            data={'user': uID, 'dose': '2nd', 'notified': False, 'confirmed': False})
        if s2.is_valid():
            s2.create(validated_data=s2.validated_data)

    def update(uID, dose, data: dict):
        for d in dose:
            u = TABLES["TI"].objects.get(user=uID, dose=d)
            s = SERIALIZERS["TI"](u, data=data, partial=True)
            if s.is_valid(raise_exception=True):
                s.update(u, validated_data=s.validated_data)
