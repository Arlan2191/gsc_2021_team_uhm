from collections import OrderedDict
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from API.services import CreatePersonnelService, EligibilityService, NotificationService, SMSService, DatastoreService, TrackingService
from SMS.library import defaultResponse
from projectBakuna.environment import globeConfig, TABLES, SERIALIZERS
from django.http import JsonResponse, HttpResponse
from requests import post
from SMS.views import SMSView
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, OR
from threading import Thread
import json


class DashboardAPIView(APIView):
    # permission_required = ('API.view_eligibility_status', 'API.view_tracking_information', 'API.view_vaccination_site', 'API.view_vaccination_session', 'API.add_vaccination_site', 'API.add_vaccination_session',
    #                        'API.change_eligibility_status', 'API.change_tracking_information', 'API.change_vaccination_site', 'API.change_vaccination_session', 'API.delete_vaccination_site', 'API.delete_vaccination_session')
    permission_classes = (AllowAny,)
    # serializer_class = None

    def get(self, request):
        try:
            table = request.GET.get('name', None)
            # and request.user.is_authenticated and request.user.is_staff and request.user.has_perms(('API.view_eligibility_status', 'API.view_tracking_information', 'API.view_vaccination_site', 'API.view_vaccination_session')):
            if table in ['ES', 'EA', 'PI', 'TI', 'VS', 'VSS']:
                id = request.GET.get('id', None)
                u_id = request.user.id
                if u_id is not None:
                    isProfile = request.GET.get('isProfile', False)
                    if id is None and table != 'TI' and table != 'PI' and table != 'EA':
                        instance = TABLES["PRI"].objects.get(pk=u_id)
                        if table == 'ES':
                            data = TABLES[table].objects.filter(
                                assigned_to=u_id, status="P")
                        elif table == 'VS':
                            data = TABLES[table].objects.filter(
                                region=instance.organization_region, province=instance.organization_province, municipality=instance.organization_municipality)
                        elif table == 'VSS':
                            instances = TABLES["VS"].objects.filter(
                                region=instance.organization_region, province=instance.organization_province, municipality=instance.organization_municipality)
                            data = []
                            for i in instances:
                                data += TABLES["VSS"].objects.filter(site=i.pk)
                    elif id != 0:
                        if table == 'TI':
                            print("HERE")
                            data = TABLES[table].objects.filter(user=int(id))
                        else:
                            data = [TABLES[table].objects.get(pk=int(id))]
                else:
                    return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
                if data is not None:
                    query = [SERIALIZERS[table](e).data for e in data]
                return JsonResponse({"query_result": self.__format(table, id, query, isProfile)}, status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def __format(self, table, id, query, isProfile):
        if table == 'PI' and not isProfile:
            query = [{"id": id, "sex": x["sex"], "birthdate": x["birthdate"],
                      "occupation": x["occupation"], "barangay": x["barangay"]} for x in query]
        return query

    def post(self, request):
        try:
            table = request.GET.get('name', None)
            # and request.user.is_authenticated and request.user.is_staff and request.user.has_perms(('API.add_vaccination_site', 'API.add_vaccination_session')):
            if table in ['VS', 'VSS', 'TI']:
                data = request.data
                serializer = SERIALIZERS[table](data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.create(serializer.validated_data)
                    return HttpResponse(status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
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
                        _ = TrackingService.update(id, dose, data)
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
    permission_classes = (AllowAny,)
    service = DatastoreService()

    def get(self, request):
        try:
            table = request.GET.get('name', None)
            if table is not None:
                id = request.GET.get('id', None)
                if id is not None:
                    if table == 'R':
                        return JsonResponse(self.service.getResponse(int(id)), status=status.HTTP_200_OK)
                else:
                    if table == 'C':
                        return JsonResponse(self.service.getCities(), status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            table = request.GET.get('name', None)
            if table is not None:
                id = request.GET.get('id', None)
                data = request.data
                if id is not None and data is not None:
                    if table == 'R':
                        _ = self.service.postResponse(id, data)
                        return HttpResponse(status=status.HTTP_200_OK)
                    elif table == 'S':
                        _ = self.service.postSession(id, data)
                        return HttpResponse(status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            table = request.GET.get('name', None)
            if table is not None:
                id = request.GET.get('id', None)
                if id is not None:
                    data = request.data
                    if table == 'S':
                        _ = self.service.updateSession(id, data)
                        return HttpResponse(status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SMSSubscriptionAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
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
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data
            return JsonResponse({'valid': SMSService.verify(data)}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PersonnelRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data
            username, PIN = CreatePersonnelService.handle(data)
            return JsonResponse({"user": {"username": username, "PIN": PIN}}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"errors": {"error": str(e)}}, status=status.HTTP_200_OK)


class NotificationAPIView(APIView):  # TODO
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            isOrdered = request.GET.get("isOrdered", False)
            filters = dict(request.data) if not isOrdered else OrderedDict(
                [(k, v) for k, v in dict(request.data).items()])
            recipients = NotificationService.get()
        except:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestingAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        command = request.data.get("command")
        table = request.GET.get("name")
        data = TABLES[table].objects.raw(command)
        return JsonResponse({"result": [str(x.pk) for x in data]}, status=status.HTTP_200_OK)
