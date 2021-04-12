import time
import re

from django.http.request import QueryDict
from SMS.views import SMSView
from django.db.models.query import QuerySet
from API.models import Local_Government_Units
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from API.services import ConfirmationService, CreatePersonnelService, EligibilityService, SMSService, DatastoreService, TrackingService
from SMS.library import defaultResponse
from projectBakuna.environment import globeConfig, TABLES, SERIALIZERS, ENGINE
from aldjemy import core
from sqlalchemy.sql import text
from django.http import JsonResponse, HttpResponse
from requests import post
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, OR
from threading import Thread


class DashboardAPIView(APIView):
    """
    This API view includes GET, POST, PUT, and DELETE requests for the SQL database tables.
    """

    # permission_required = ('API.view_eligibility_status', 'API.view_tracking_information', 'API.view_vaccination_site', 'API.view_vaccination_session', 'API.add_vaccination_site', 'API.add_vaccination_session',
    #                        'API.change_eligibility_status', 'API.change_tracking_information', 'API.change_vaccination_site', 'API.change_vaccination_session', 'API.delete_vaccination_site', 'API.delete_vaccination_session')
    permission_classes = (AllowAny,)
    # serializer_class = None

    def get(self, request):
        """
        This method handles get requests only for the following tables:
            1. Eligibility Status (ES)
            2. Eligibility Applications (EA)
            3. Personal Information (PI)
            4. Tracking Information (TI)
            5. Vaccination Sites (VS)
            6. Vaccination Sessions (VSS)

        Data are classified for each LGU and can only be seen by that LGU. How I implemented that is by assigning an ID for
        each registered LGU and labeling each entry with that ID.
        """
        try:
            table = request.GET.get('name', None)
            # and request.user.is_authenticated and request.user.is_staff and request.user.has_perms(('API.view_eligibility_status', 'API.view_tracking_information', 'API.view_vaccination_site', 'API.view_vaccination_session')):
            if table in ['ES', 'EA', 'PI', 'TI', 'VS', 'VSS']:
                id = request.GET.get('id', None)
                lgu_id = request.user.lgu_id.lgu_id
                if lgu_id is not None:
                    isProfile = request.GET.get('isProfile', False)
                    u_id = request.user.id
                    if id is None and table != 'TI' and table != 'PI' and table != 'EA':
                        if table == 'ES':
                            data = TABLES[table].objects.filter(
                                assigned_to=u_id, status="P", lgu_id=lgu_id)
                        elif table == 'VS':
                            data = TABLES[table].objects.filter(lgu_id=lgu_id)
                        elif table == 'VSS':
                            instances = TABLES["VS"].objects.filter(
                                lgu_id=lgu_id)
                            data = []
                            for i in instances:
                                data += TABLES["VSS"].objects.filter(site=i.pk)
                    elif id != 0:
                        if table == 'TI':
                            data = TABLES[table].objects.filter(user=int(id))
                        else:
                            data = [TABLES[table].objects.get(pk=int(id))]
                else:
                    return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
                if data is not None:
                    query = [SERIALIZERS[table](e).data for e in data]
                return JsonResponse({"query_result": self.__format(table, id, query, isProfile)}, status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def __format(self, table, id, query, isProfile):
        if table == 'PI' and not isProfile:
            query = [{"id": id, "sex": x["sex"], "birthdate": x["birthdate"],
                      "occupation": x["occupation"], "barangay": x["barangay"]} for x in query]
        return query

    def post(self, request):
        """
        This method handles post requests only for the following tables:
        1. Vaccination Sites
        2. Vaccination Sessions
        3. Tracking Information

        Staff users are only allowed to create entries for the indicated tables in the dashboard.
        """
        try:
            table = request.GET.get('name', None)
            lgu_id = request.user.lgu_id.lgu_id
            # and request.user.is_authenticated and request.user.is_staff and request.user.has_perms(('API.add_vaccination_site', 'API.add_vaccination_session')):
            if table in ['VS', 'VSS', 'TI'] and lgu_id is not None:
                data = dict([(k, v[0])for k, v in request.data.items()])
                data["lgu_id"] = lgu_id
                serializer = SERIALIZERS[table](data=data)
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.create(serializer.validated_data)
                    if table == 'VSS':
                        Thread(target=DatastoreService().initSessionConfirmations, args=[
                               lgu_id, instance.pk]).start()
                    return HttpResponse(status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """
        This method handles put requests only for the following tables:
            1. Eligibility Status (ES)
            2. Eligibility Application (EA)
            3. Tracking Information (TI)
            4. Vaccination Sites (VS)
            5. Vaccination Sessions (VSS)

        Staff users must update the ES entry of each user assigned to them that still has P (pending status) in their 
        application. For every application pending, reviewing, and reviewed the EA table must be updated. The reviewing
        column of EA must only contain one user ID that is currently reviewed for if the reviewing staff exits and logins
        again, the changes will neither be saved nor discarded and will be prompted.

        Staff users can only update VS if their site id is not referenced in the VSS table. A VSS entry is only mutable 2 weeks
        before it is held. Only one change is allowed for all VSS entries. The total user confirmations will be considered final 
        at least two days before the vaccination session.

        Staff users can only update TI during a vaccination session, or if with higher permission.
        """
        try:
            table = request.GET.get('name', None)
            # and request.user.is_authenticated and request.user.is_staff and request.user.has_perms(('API.change_eligibility_status', 'API.change_tracking_information', 'API.change_vaccination_site', 'API.change_vaccination_session')):
            if table in ['ES', 'EA', 'TI', 'VS', 'VSS']:
                id = request.GET.get('id', None)
                data = request.data
                dose = request.GET.get('dose', None)
                if id is not None:
                    if table == 'ES':
                        _ = EligibilityService.update(id, data)
                        return HttpResponse(status=status.HTTP_200_OK)
                    elif table == 'TI' and dose is not None:
                        _ = TrackingService.update(id, [dose], data)
                        return HttpResponse(status=status.HTTP_200_OK)
                    else:
                        instance = TABLES[table].objects.get(pk=id)
                        if instance is not None:
                            serializer = SERIALIZERS[table](
                                data=data, partial=True)
                            if serializer.is_valid(raise_exception=True):
                                serializer.update(
                                    instance, serializer.validated_data)
                                return HttpResponse(status=status.HTTP_200_OK)
                        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """
        This method handles delete requests only for the following tables:
            1. Vaccination Sites (VS)
            2. Vaccination Sessions (VSS)

        VSS entries can only be deleted within the next 48 hours and will be considered final otherwise.    
        """
        try:
            table = request.GET.get('name')
            # and request.user.is_authenticated and request.user.is_staff and request.user.has_perms(('API.delete_vaccination_site', 'API.delete_vaccination_session')):
            if table in ['VS', 'VSS']:
                id = request.GET.get('id')
                if id is not None:
                    instance = TABLES[table].objects.get(pk=id)
                    data = instance.delete()
                    return JsonResponse({"query_result": data}, status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DatastoreAPIView(APIView):
    """
    This API view includes GET, and POST requests for the GCP Datastore databases.
    """
    permission_classes = (AllowAny,)
    service = DatastoreService()

    def get(self, request):
        """
        This method handles get requests only for the following tables:
            1. Medical History Responses (MHR)
            2. LGU Addresses

        Request for multiple MHRs is prohibited.
        """
        try:
            table = request.GET.get('name', None)
            if table is not None:
                id = request.GET.get('id', None)
                if id is not None:
                    if table == 'MHR':
                        return JsonResponse(self.service.getResponse(int(id)), status=status.HTTP_200_OK)
                else:
                    if table == 'LGU':
                        return JsonResponse(self.service.getCities(), status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        This method handles post requests only for the following tables:
            1. Medical History Responses (MHR)

        This method must only accept requests from the WMS Platform.
        """
        try:
            table = request.GET.get('name', None)
            if table is not None:
                id = request.GET.get('id', None)
                data = request.data
                if id is not None and data is not None:
                    if table == 'MHR':
                        _ = self.service.postResponse(id, data)
                        return HttpResponse(status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SMSSubscriptionAPIView(APIView):
    """
    This API view includes GET, and POST requests for the Globe Labs Subscription.
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        This method handles get requests from the Globe Labs API and must only accept from such host.
        It is only used for subscribing to the service.
        """
        try:
            code = request.GET.get('code', None)
            if code is not None:
                query_result = post("https://developer.globelabs.com.ph/oauth/access_token?app_id={}&app_secret={}&code={}".format(
                    globeConfig.get("appId"), globeConfig.get("appSecret"), code)).json()
                auth_token = query_result['access_token']
                mobile_number = query_result['subscriber_number']
            else:
                auth_token = request.GET.get('access_token')
                mobile_number = request.GET.get('subscriber_number')
            isSub, verification_code = SMSService.subsribe(
                {"mobile_number": "+63" + mobile_number, "auth_token": auth_token})
            if isSub:
                if code is not None:
                    # Thread(target=SMSView.asyncSendSMS, args=[
                    #     auth_token, "+63" + mobile_number, defaultResponse.get('defaultVerify').format(verification_code)]).start()
                    return render(request, "verify.html", {"user_number": mobile_number})
                else:
                    # Thread(target=SMSView.asyncSendSMS, args=[
                    #     auth_token, "+63" + mobile_number]).start()
                    return HttpResponse(status=status.HTTP_200_OK)
            else:
                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        This method handles post requests from the Globe Labs API and must only accept from such host.
        It is only used for unsubscribing to the service.
        """
        try:
            data = request.data
            if data.get('unsubscribed') is not None:
                SMSService.unsubcribe(
                    "+63" + data["unsubscribed"]["subscriber_number"])
                return HttpResponse(status=status.HTTP_200_OK)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SMSVerificationAPIView(APIView):
    """
    This API view handles OTP Verification for the Web and Messenger Forms.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data
            return JsonResponse({'valid': SMSService.verify(data)}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LGURegistrationAPIView(APIView):
    """
    This API View handles the registration form for LGU staff.
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            region = request.GET.get("region", None)
            province = request.GET.get("province", None)
            municipality = request.GET.get("municipality", None)
            if region and province and municipality:
                instance = TABLES["LGU"].objects.get(
                    region=region, province=province, municipality=municipality)
                return JsonResponse({"lgu_id": instance.pk}, status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            isLGU = request.GET.get('LGU', False)
            data = request.data
            lgu_id = data.get("lgu_id", None)
            if lgu_id is not None:
                if not isLGU:
                    try:
                        instance = TABLES["LGUA"].objects.get(pk=lgu_id)
                        if instance is not None:
                            username, PIN = CreatePersonnelService.handle(data)
                            return JsonResponse({"user": {"username": username, "PIN": PIN}}, status=status.HTTP_200_OK)
                    except ObjectDoesNotExist:
                        return JsonResponse({"errors": {"error": "LGU does not exist. Please register your LGU first."}}, status=status.HTTP_200_OK)
                else:
                    instances = TABLES["PRI"].objects.filter(lgu_id=lgu_id)
                    if not len(instances):
                        username, PIN = CreatePersonnelService.register(data)
                        return JsonResponse({"user": {"username": username, "PIN": PIN}}, status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"errors": {"error": str(e)}}, status=status.HTTP_200_OK)


class NotificationAPIView(APIView):  # TODO
    """
    This API View handles the notification of users for created and updated VSS, confirmation for VSS, and status of
    reviewed applications.
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            lgu_id = request.user.lgu_id.lgu_id
            if lgu_id is not None:
                vss_id = request.GET.get("VSS", None)
                instance = SERIALIZERS["VSS"](
                    TABLES["VSS"].objects.get(pk=vss_id)).data
                if instance is not None:
                    max_cap = instance.get("max_cap", None)
                    dose = instance.get("dose", None)
                    birth_range = instance.get("birth_range", None).split(',')
                    priority = instance.get("priority", None).split(',')
                    barangay = instance.get("target_barangay", None).split(',')
                    if max_cap is not None:
                        filters = ""
                        if priority is not None:
                            if len(priority):
                                if len(priority[0]):
                                    filters += " AND (" + " ".join(["e.priority={} OR".format(priority[i]) if i < len(
                                        priority) - 1 else "e.priority={}".format(priority[i]) for i in range(len(priority)) if len(priority[i])]) + ")"
                        if barangay is not None:
                            if len(barangay):
                                if len(birth_range[0]):
                                    filters += " AND (" + " ".join(["p.barangay={} OR".format(barangay[i]) if i < len(
                                        priority) - 1 else "p.barangay={}".format(barangay[i]) for i in range(len(barangay)) if len(barangay[i])]) + ")"
                        if birth_range is not None:
                            if len(birth_range):
                                if len(birth_range[0]) == 10:
                                    filters += " AND (p.birthdate >= CAST('{}' AS DATE) AND p.birthdate <= CAST('{}' AS DATE))".format(
                                        *birth_range)
                        query = text(
                            "SELECT m.mobile_number, auth_token, email, first_name, p.id FROM ((personal_information AS p INNER JOIN auth_mobile_number AS m ON p.mobile_number=m.mobile_number AND (m.auth_token!='Unsubscribed' OR p.email!='N/A')) INNER JOIN eligibility_status AS e ON p.id=e.id_id) INNER JOIN tracking_information as t ON t.user_id=p.id WHERE (t.dose='{}' AND (t.status='P' OR t.status='M')) AND (e.status='G' OR e.status='G@R') AND p.lgu_id_id={}{} LIMIT {}".format(dose, lgu_id, filters, max_cap))
                        connection = ENGINE.connect()
                        recipients = connection.execute(query).fetchall()
                        Thread(target=self.notify, args=[
                               recipients, instance]).start()
                        return HttpResponse(status=status.HTTP_200_OK)
                    else:
                        return JsonResponse({"errors": {"error": "Maximum number of recipients must be defined"}}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"errors": {"error": "Vaccination Session not found"}}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"errors": {"error": "An LGU ID must be provided"}}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def notify(self, recipients: list, data: dict):
        time.sleep(0.01)
        site = TABLES["VS"].objects.get(pk=data.get("site"))
        address = "{}, {}".format(site.site_address, site.barangay)
        for r in recipients:
            message = defaultResponse["defaultSessionNotification"].format(
                r[3], data.get("date"), data.get("time"), address)
            print(message)
            # _ = SMSView.sendSMSMessage(r[0], r[1], message)
            instance = TABLES["TI"].objects.get(
                user_id=r[4], dose=data.get("dose"))
            serializer = SERIALIZERS["TI"](
                instance, data={"notified": True, "session": data.get("vs_id")}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.update(instance, serializer.validated_data)


# class InitiateLGUAPIView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         try:
#             data = request.data
#             keys = data.keys()
#             for k in keys:
#                 r = data[k]["region_name"]
#                 provinces = data[k]["province_list"].keys()
#                 for p in provinces:
#                     municipalities = data[k]["province_list"][p]["municipality_list"].keys(
#                     )
#                     for m in municipalities:
#                         _ = Local_Government_Units.objects.create(
#                             region=r, province=p, municipality=m)
#             return HttpResponse(status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InitiateDatabasePIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data
            keys = data.keys()
            for k in keys:
                r = data[k]["region_name"]
                provinces = data[k]["province_list"].keys()
                for p in provinces:
                    municipalities = data[k]["province_list"][p]["municipality_list"].keys(
                    )
                    for m in municipalities:
                        _ = Local_Government_Units.objects.create(
                            region=r, province=p, municipality=m)
            return HttpResponse(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class TestingAPIView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         command = request.data.get("command")
#         table = request.GET.get("name")
#         data = TABLES[table].objects.raw(command)
#         return JsonResponse({"result": [str(x.pk) for x in data]}, status=status.HTTP_200_OK)

# class TestConfirmAPIView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         text = request.data.get("message")
#         message = re.fullmatch(
#             "^\s*CONFIRM\s+<?(([0-9]{2})\-([0-9]{4})\-([0-9]+))>?\s*$", text)
#         lgu_id = message.group(3)
#         uID = message.group(4)
#         instance = ConfirmationService.handle(uID, lgu_id)
#         site = TABLES["VS"].objects.get(pk=instance.site.pk)
#         address = "{}, {}".format(site.site_address, site.barangay)
#         print(defaultResponse["defaultSessionConfirmation"].format(
#             instance.date, instance.time, address, ""))
#         return HttpResponse(status=status.HTTP_200_OK)
