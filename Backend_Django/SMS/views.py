from django.http.request import QueryDict
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View
from rest_framework import status
from projectBakuna.environment import globeConfig, dialogflowConfig, EMAIL, HOTLINE, TABLES, SERIALIZERS
from projectBakuna.exceptions import IncorrectPINException, InvalidNumber, MaxEntryException
from google.cloud.dialogflow_v2.types import TextInput, QueryInput
from google.cloud.dialogflow_v2 import SessionsClient
from google.oauth2 import service_account
from django.http import HttpResponse
from SMS.library import defaultResponse
from requests import post
from API.services import CreateService, SMSService
from threading import Thread
from django.core.exceptions import ObjectDoesNotExist
import random
import time
import json
import re

sessionCredential = service_account.Credentials.from_service_account_info(
    dialogflowConfig)
sessionClient = SessionsClient(credentials=sessionCredential)


class SMSView(View):

    def sendSMSMessage(mobile_number: str, access_token: str, message: str):
        senderAddress = globeConfig.get("shortCodeCrossTelco")[-4:]
        data = {"outboundSMSMessageRequest": {"clientCorrelator": "0000", "senderAddress": str(senderAddress),
                                              "outboundSMSTextMessage": {"message": "{}".format(message)}, "address": "tel: {}".format(str(mobile_number))}}
        senderAddress = globeConfig.get("shortCode")[-4:]
        _ = post(url="https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/{}/requests?access_token={}".format(
            senderAddress, access_token), json=data)

    def asyncSendSMS(access_token, mobile_number: str, message=None):
        time.sleep(0.01)
        if message is None:
            SMSView.sendSMSMessage(mobile_number, access_token,
                                   defaultResponse["defaultWelcome"])
        else:
            SMSView.sendSMSMessage(mobile_number, access_token, message)

    def checkResponse(query_text: str, parameters: str):
        try:
            params = dict(parameters)
            error_message = "Oops! It seems like your {} is invalid. Please check your text if {}"
            if query_text.upper() == "APPLY":
                return "Your Covid-19 Vaccination Application is starting. When you receive \"Application Sent\" with your reference ID, that means your application was successfully validated and will now undergo our medical team's eligibility check.\n\n"
            elif params["personalInfo"] == "" and params["survey1response"] == "" and params["survey2response"] == "" and params["survey3response"] == "":
                return error_message.format("personal information", "the numbering is correct (1-12); your first, middle, and last name do not have special characters or numbers; your birthdate is of the format YYYY-MM-DD; and your input did not interchange\n\n")
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

    def saveResponse(mobile_number, auth_token, response: dict):
        personal_info = dict([(y, x) if y != "email" else (y, "") if x == "N/A" else (y, x) for x, y in zip(
            re.split("\s?[0-9]{1,2}\.\s+", response["personalInfo"])[1:], ["first_name", "middle_name", "last_name", "birthdate", "sex", "occupation", "email", "region", "province", "municipality", "barangay", "home_address"])])
        personal_info["mobile_number"] = mobile_number
        response = dict([(str(k), v) for k, v in zip(list(range(1, 13)), re.split("\s?[0-9]{1,2}\.\s+", response["survey1response"])[1:])] + [(str(k), v) for k, v in zip(list(range(
            13, 19)), re.split("\s?[0-9]{1,2}\.\s+", response["survey2response"])[1:])] + [(str(k), v) for k, v in zip(list(range(19, 33)), re.split("\s?[0-9]{1,2}\.\s+", response["survey3response"])[1:])])
        try:
            return CreateService.handle(response, personal_info)
        except MaxEntryException as e:
            SMSView.sendSMSMessage(mobile_number, auth_token, str(e))
            return None
        except InvalidNumber as e:
            SMSView.sendSMSMessage(
                mobile_number, auth_token, defaultResponse["invalidNum"].format(str(e).lower()))
            return None
        except Exception as e:
            raise e

    @require_POST
    @csrf_exempt
    def receiveSMS(request):
        try:
            message = json.loads(request.body)
            dataQuery = TABLES["AM"].objects.get(pk=int(str(
                message["inboundSMSMessageList"]["inboundSMSMessage"][0]["senderAddress"]).split(":")[-1].replace("+", "")))
            text = message["inboundSMSMessageList"]["inboundSMSMessage"][0]["message"]
            if "STATUS" in text:
                try:
                    message = re.fullmatch(
                        "^\s*STATUS\s+<?(([0-9]{2})\-([0-9]{4})\-([0-9]+))>?\s+<?(.+)>?\s*$", text)
                    rID = message.group(1)
                    uID = message.group(4)
                    PIN = message.group(5)
                    firstName, statusObj = SMSService.getStatusObject(
                        uID, dataQuery.mobile_number, rID, PIN)
                    SMSView.sendSMSMessage(dataQuery.mobile_number, dataQuery.auth_token, defaultResponse["defaultStatusCheck"].format(
                        firstName, statusObj.get_status_display(), statusObj.reason))
                    return HttpResponse(status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    SMSView.sendSMSMessage(
                        dataQuery.mobile_number, dataQuery.auth_token, defaultResponse["errorID"])
                    return HttpResponse(status=status.HTTP_200_OK)
                except IncorrectPINException:
                    SMSView.sendSMSMessage(
                        dataQuery.mobile_number, dataQuery.auth_token, defaultResponse["errorPIN"])
                    return HttpResponse(status=status.HTTP_200_OK)
                except Exception as e:
                    print(str(e))
                    SMSView.sendSMSMessage(
                        dataQuery.mobile_number, dataQuery.auth_token, defaultResponse["defaultError"])
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
                if dialogflowResponse.query_result.all_required_params_present and dialogflowResponse.query_result.intent.display_name == "Save SMS Form":
                    params = dict(dialogflowResponse.query_result.parameters)
                    try:
                        rID, PIN = SMSView.saveResponse(
                            dataQuery.mobile_number, dataQuery.auth_token, params)
                        if rID != None and PIN != None:
                            if dialogflowResponse.query_result.fulfillment_text[0:11] == "Application":
                                SMSView.sendSMSMessage(dataQuery.mobile_number, dataQuery.auth_token, dialogflowResponse.query_result.fulfillment_text.format(
                                    rID, PIN, dataQuery.mobile_number, EMAIL, HOTLINE))
                            else:
                                SMSView.sendSMSMessage(
                                    dataQuery.mobile_number, dataQuery.auth_token, dialogflowResponse.query_result.fulfillment_text)
                        return HttpResponse(status=status.HTTP_200_OK)
                    except Exception as e:
                        print(e)
                        SMSView.sendSMSMessage(
                            dataQuery.mobile_number, dataQuery.auth_token, defaultResponse["defaultError"])
                        return HttpResponse(status=status.HTTP_200_OK)
                elif dialogflowResponse.query_result.fulfillment_text[0:2] == "{}" and dialogflowResponse.query_result.intent.display_name == "Save SMS Form":
                    if text == "APPLY" and dataQuery.amount_entry == 10:
                        SMSView.sendSMSMessage(
                            dataQuery.mobile_number, dataQuery.auth_token, str(MaxEntryException()))
                        return HttpResponse(status=status.HTTP_200_OK)
                    SMSView.sendSMSMessage(dataQuery.mobile_number, dataQuery.auth_token,
                                           dialogflowResponse.query_result.fulfillment_text.format(prefix))
                else:
                    SMSView.sendSMSMessage(
                        dataQuery.mobile_number, dataQuery.auth_token, dialogflowResponse.query_result.fulfillment_text)
                return HttpResponse(status=status.HTTP_200_OK)
        except:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @csrf_exempt
    def receiveUserToken(request):
        if request.method == 'GET':
            try:
                dataQuery = QueryDict(str(request.GET.urlencode()))
                if "code" in dataQuery.keys():
                    dataQuery = post("https://developer.globelabs.com.ph/oauth/access_token?app_id={}&app_secret={}&code={}".format(
                        globeConfig.get("appId"), globeConfig.get("appSecret"), dataQuery.get("code"))).json()
                elif "access_token" in dataQuery.keys():
                    dataQuery = dataQuery.dict()
                else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
                if SMSService.subsribe({"mobile_number": "+63" + dataQuery["subscriber_number"], "auth_token": dataQuery["access_token"]}):
                    Thread(target=SMSView.asyncSendSMS, args=[
                        dataQuery["access_token"], "+63" + dataQuery["subscriber_number"]]).start()
                    return HttpResponse(status=status.HTTP_200_OK)
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                dataQuery = dict(json.loads(request.body))
                if "unsubscribed" in dataQuery.keys():
                    SMSService.unsubcribe(
                        "+63" + dataQuery["unsubscribed"]["subscriber_number"])
                    return HttpResponse(status=status.HTTP_200_OK)
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
