from datetime import datetime
from os import stat
from django.http.request import QueryDict
from django.http.response import HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpRequest
from django.views import View
from rest_framework import status
from projectBakuna.environment import globeConfig, dialogflowConfig, surveySMSFormConfig, datastoreConfig
from projectBakuna.exceptions import IncorrectResponse, IncompleteResponse
from google.cloud.dialogflow_v2.types import TextInput, QueryInput
from google.cloud.dialogflow_v2 import SessionsClient
from google.cloud import datastore
from google.oauth2 import service_account
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from requests import get, post
from FORMS.serializers import AuthMobileNumberSerializer, PersonalInformationSerializer
from API.serializers import EligibilityStatusSerializer
from FORMS.models import Personal_Information, Auth_Mobile_Number
from API.models import Vaccination_Site, Eligibility_Status, Tracking_Information
from threading import Thread
from multiprocessing import Process
from django.core.exceptions import ObjectDoesNotExist
import time
import json
import re

sessionCredential = service_account.Credentials.from_service_account_info(
    dialogflowConfig)
datastoreCredential = service_account.Credentials.from_service_account_info(
    datastoreConfig)
sessionClient = SessionsClient(credentials=sessionCredential)
datastoreClient = datastore.Client(credentials=datastoreCredential)
pi_fields = ["first_name", "middle_name", "last_name", "birthdate",
             "sex", "home_address", "city", "barangay"]


class SMSView(View):

    def formatSMSMessage(mobile_number: str, message: str):
        senderAddress = globeConfig.get("shortCodeCrossTelco")[-4:]
        data = {"outboundSMSMessageRequest": {"clientCorrelator": "0000", "senderAddress": str(senderAddress),
                                              "outboundSMSTextMessage": {"message": "{}".format(message)}, "address": "tel: {}".format(str(mobile_number))}}
        return data

    def sendSMS(access_token, data: dict):
        senderAddress = globeConfig.get("shortCode")[-4:]
        access_token = access_token
        try:
            response = post(url="https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/{}/requests?access_token={}".format(
                senderAddress, access_token), json=data).json()
            return status.HTTP_200_OK
        except:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def asyncSendSMS(access_token, mobile_number: str):
        time.sleep(0.01)
        senderAddress = globeConfig.get("shortCode")[-4:]
        access_token = access_token
        message = "Text \"APPLY\" to 225657031 to begin your Covid-19 Vaccination Application. If you have already applied, text \"STATUS\" to 225657031 to check the status of your application. For other concerns, please contact us via our email: arlan.german.ag@gmail.com or our hotline: +639995529611"
        data = SMSView.formatSMSMessage(mobile_number, message)
        try:
            response = post(url="https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/{}/requests?access_token={}".format(
                senderAddress, access_token), json=data).status_code
            if response == 200:
                return status.HTTP_200_OK
            else:
                return status.HTTP_500_INTERNAL_SERVER_ERROR
        except:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def checkResponse(query_text: str, parameters: str):
        try:
            params = dict(parameters)
            error_message = "Oops! It seems like your {} is invalid. Please check your text if {}"
            if query_text.upper() == "APPLY":
                return "Your Covid-19 Vaccination Application is starting. When you receive \"Application Sent\" with your reference ID, that means your application was successfully validated and will now undergo our medical team's eligibility check.\n\n"
            elif params["personalInfo"] == "" and params["survey1response"] == "" and params["survey2response"] == "" and params["survey3response"] == "":
                return error_message.format("personal information", "the numbering is correct (1-8); your first, middle, and last name do not have special characters or numbers; and your birthdate is of the format YYYY-MM-DD.\n\n")
            elif params["personalInfo"] != "" and params["personalInfo"] != query_text and params["survey1response"] == "" and params["survey2response"] == "" and params["survey3response"] == "":
                return error_message.format("response", "the numbering is correct (1-12) and your answers are either Y, or N.\n\n")
            elif params["personalInfo"] != "" and params["survey1response"] != query_text and params["survey1response"] != "" and params["survey2response"] == "" and params["survey3response"] == "":
                return error_message.format("response", "the numbering is correct (13-18) and your answers are either Y, N, or U.\n\n")
            elif params["personalInfo"] != "" and params["survey2response"] != query_text and params["survey1response"] != "" and params["survey2response"] != "" and params["survey3response"] == "":
                return error_message.format("response", "the numbering is correct (19-32) and your answers are either Y, or N.\n\n")
            else:
                return ""
        except Exception as e:
            return ""

    def saveStatus(uID: int):
        time.sleep(0.01)
        data = {"id": uID, "status": "pending",
                "reason": "Our medical team has yet to review your application"}
        es_serializer = EligibilityStatusSerializer(data=data)
        if es_serializer.is_valid(raise_exception=True):
            es_serializer.create(validated_data=es_serializer.validated_data)

    def saveEntity(uID, response: dict):
        time.sleep(0.01)
        eKey = datastoreClient.key('Records', int(uID))
        task = datastore.Entity(key=eKey)
        task["Response"] = {}
        for key in response.keys():
            if key != "personalInfo":
                keys, vals = re.findall(
                    "[0-9]{1,2}", response[key]), re.split("\s?[0-9]{1,2}\.\s?", response[key])[1:]
                for k, v in zip(keys, vals):
                    task["Response"][k] = v
        task["Datetime"] = str(datetime.now())
        datastoreClient.put(task)

    def saveResponse(mobile_number, response: dict):
        personal_info = dict([(y, x)for x, y in zip(
            re.split("\s?[0-9]{1,2}\.\s?", response["personalInfo"])[1:], pi_fields)])
        personal_info["mobile_number"] = mobile_number
        pi_serializer = PersonalInformationSerializer(
            data=personal_info)
        try:
            if pi_serializer.is_valid(raise_exception=True):
                uID = pi_serializer.create(
                    validated_data=pi_serializer.validated_data).id
                Thread(target=SMSView.saveStatus, args=[uID]).start()
                Thread(target=SMSView.saveEntity, args=[uID, response]).start()
                return uID
        except Exception as e:
            raise e

    @require_POST
    @csrf_exempt
    def receiveSMS(request):
        try:
            message = json.loads(request.body)
            dataQuery = Auth_Mobile_Number.objects.get(pk=int(str(
                message["inboundSMSMessageList"]["inboundSMSMessage"][0]["senderAddress"]).split(":")[-1].replace("+", "")))
            text = message["inboundSMSMessageList"]["inboundSMSMessage"][0]["message"]
            if "STATUS" in text:
                try:
                    uID = int(re.findall("[0-9]+$", text)[0])
                    entity = Personal_Information.objects.get(id=uID)
                    if dataQuery.mobile_number == entity.mobile_number:
                        e_status = Eligibility_Status.objects.get(id=uID)
                        data = SMSView.formatSMSMessage(
                            dataQuery.mobile_number, "Greetings {}, the eligibility status of your Covid-19 vaccine application is {} due to the following:\n\n\"{}\",\n\nas pointed out by our medical team. If you have any issues or concerns, please do reach us at our email: arlan.german.ag@gmail.com and our hotline: +639995529611".format(entity.first_name, e_status.status, e_status.reason))
                        _ = SMSView.sendSMS(access_token=dataQuery.auth_token,
                                            data=data)
                        return HttpResponse(status=status.HTTP_200_OK)
                    else:
                        raise ObjectDoesNotExist
                except ObjectDoesNotExist:
                    data = SMSView.formatSMSMessage(
                        dataQuery.mobile_number, "Sorry, it seems like this Unique ID does not belong to your mobile number or does not exist at all. Please check your Unique ID if it is correct and try again.")
                    _ = SMSView.sendSMS(access_token=dataQuery.auth_token,
                                        data=data)
                    return HttpResponse(status=status.HTTP_200_OK)
                except:
                    data = SMSView.formatSMSMessage(
                        dataQuery.mobile_number, "Our deepest apologies, our servers encountered an error. Please try again later.")
                    _ = SMSView.sendSMS(
                        access_token=dataQuery.auth_token, data=data)
                    return HttpResponse(status=status.HTTP_200_OK)
            else:
                session = sessionClient.session_path(
                    dialogflowConfig["project_id"], dataQuery.mn_id)
                text_input = TextInput(text=text, language_code='en-US')
                query_input = QueryInput(text=text_input)
                dialogflowResponse = sessionClient.detect_intent(request={
                    "session": session, "query_input": query_input})
                prefix = SMSView.checkResponse(
                    dialogflowResponse.query_result.query_text, dialogflowResponse.query_result.parameters)
                if dialogflowResponse.query_result.all_required_params_present:
                    params = dict(dialogflowResponse.query_result.parameters)
                    try:
                        uID = SMSView.saveResponse(
                            dataQuery.mobile_number, params)
                        data = SMSView.formatSMSMessage(
                            dataQuery.mobile_number, dialogflowResponse.query_result.fulfillment_text.format(uID, dataQuery.mobile_number))
                        _ = SMSView.sendSMS(
                            access_token=dataQuery.auth_token, data=data)
                        return HttpResponse(status=status.HTTP_200_OK)
                    except:
                        data = SMSView.formatSMSMessage(
                            dataQuery.mobile_number, "Our deepest apologies, our servers encountered an error. Please try again later.")
                        _ = SMSView.sendSMS(
                            access_token=dataQuery.auth_token, data=data)
                        return HttpResponse(status=status.HTTP_200_OK)
                data = SMSView.formatSMSMessage(
                    dataQuery.mobile_number, dialogflowResponse.query_result.fulfillment_text.format(prefix))
                _ = SMSView.sendSMS(access_token=dataQuery.auth_token,
                                    data=data)
                return HttpResponse(status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @csrf_exempt
    def receiveUserToken(request):
        if request.method == 'GET':
            try:
                dataQuery = QueryDict(str(request.GET.urlencode()))
                if "code" in dataQuery.keys():
                    dataQuery = post("https://developer.globelabs.com.ph/oauth/access_token?app_id={}&app_secret={}&code={}".format(
                        globeConfig.get("appId"), globeConfig.get("appSecret"), dataQuery.get("code"))).json()
                    serializer = AuthMobileNumberSerializer(
                        data={"mobile_number": "+63" + dataQuery["subscriber_number"], "auth_token": dataQuery["access_token"]})
                    if serializer.is_valid():
                        serializer.create(serializer.validated_data)
                        asyncThread = Thread(target=SMSView.asyncSendSMS, args=[
                                             dataQuery["access_token"], "+63" + dataQuery["subscriber_number"]])
                        asyncThread.start()
                        # TODO
                        return redirect("https://www.facebook.com/?mobile_number={}".format(dataQuery["subscriber_number"]))
                    else:
                        # TODO
                        return redirect("https://www.facebook.com/?error=1")
                elif "access_token" in dataQuery.keys():
                    dataQuery = dataQuery.dict()
                    serializer = AuthMobileNumberSerializer(
                        data={"mobile_number": "+63" + dataQuery["subscriber_number"], "auth_token": dataQuery["access_token"]})
                    if serializer.is_valid():
                        serializer.create(serializer.validated_data)
                        asyncThread = Thread(target=SMSView.asyncSendSMS, args=[
                                             dataQuery["access_token"], "+63" + dataQuery["subscriber_number"]])
                        asyncThread.start()
                        return HttpResponse(status=status.HTTP_200_OK)
                    else:
                        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
                else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            except:
                # TODO
                return redirect("https://www.facebook.com/?error=1", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                dataQuery = dict(json.loads(request.body))
                if "unsubscribed" in dataQuery.keys():
                    serializer = AuthMobileNumberSerializer(
                        data={"mobile_number": "+63" + dataQuery["unsubscribed"]["subscriber_number"], "auth_token": "Unsubscribed"})
                    if serializer.is_valid():
                        serializer.create(serializer.validated_data)
                        return HttpResponse(status=status.HTTP_200_OK)
                    else:
                        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            except:
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
