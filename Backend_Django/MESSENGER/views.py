from API.services import CreateService, AuthUserService, EligibilityService, SMSService
from projectBakuna.exceptions import IncompleteResponse, IncorrectResponse
from projectBakuna.environment import surveyFormConfig, EMAIL, HOTLINE, TABLES, SERIALIZERS
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.views import View
import json
import re


class MessengerView(View):

    @require_POST
    @csrf_exempt
    def postRequest(request):
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                message = json.loads(request.body)
                intent = message["queryResult"]["intent"]["displayName"]
                if intent == "Verify Mobile Number":
                    mobileNum = message["queryResult"]["parameters"]["mobileNum"] if "+63" == message["queryResult"]["parameters"]["mobileNum"][0:3] else "+63{}".format(
                        message["queryResult"]["parameters"]["mobileNum"][1:].replace(" ", ""))
                    verification = MessengerView.confirmMobileNumber(mobileNum)
                    if str(verification) == mobileNum:
                        return JsonResponse({"followupEventInput": {"name": "SaveMessengerForm", "parameters": {"mobileNum": mobileNum}, "languageCode": "en-US"}}, safe=False, status=status.HTTP_200_OK)
                    else:
                        return JsonResponse({"followupEventInput": {"name": "VerifyMobileNumber", "languageCode": "en-US"}}, safe=False, status=status.HTTP_200_OK)
                elif intent == "Check Status":
                    temp = message["queryResult"]["parameters"]["referenceID"]
                    temp = re.fullmatch(
                        "^\s*STATUS\s+<?(([0-9]{2})\-([0-9]{4})\-([0-9]+))>?\s+<?(.+)>?\s*$", temp)
                    rID = temp.group(0)
                    uID = temp.group(3)
                    PIN = message["queryResult"]["parameters"]["PIN"]
                    try:
                        if AuthUserService.login({"username": rID, "password": PIN}) is not None:
                            instance = TABLES["PI"].objects.get(pk=uID)
                            dialogFlowResponse = MessengerView.processStatusMessage(
                                uID, message, instance.first_name)
                            print(dialogFlowResponse)
                        return JsonResponse(dialogFlowResponse, safe=False, status=status.HTTP_200_OK)
                    except ValidationError as e:
                        return JsonResponse()
                else:
                    dialogFlowResponse = MessengerView.processFormMessage(
                        message=message["queryResult"])
                    return JsonResponse(dialogFlowResponse, safe=False, status=status.HTTP_200_OK)
            except:
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def processStatusMessage(uID: int, message: dict, fName: str):
        fulfillmentText = message["fulfillmentMessages"]
        instance = EligibilityService.view(uID)
        eStatus, eReason = instance.get_status_display(), instance.reason
        fulfillmentText[1]["text"]["text"][0] = fulfillmentText[1]["text"]["text"][0].format(
            fName, eStatus, eReason, EMAIL, HOTLINE)
        return fulfillmentText

    def processFormMessage(message: dict):
        intent = message["intent"]["displayName"]
        params = message["parameters"]
        survey1response = {"1": params.pop("survey1response")}
        survey2response = {"2": params.pop("survey2response")}
        survey3response = {"3": params.pop("survey3response")}
        fulfillmentText = {"fulfillmentMessages": [
            {"text": {"text": []}}]}

        if intent == "Save Messenger Form":
            try:
                MessengerView.checkResponse(
                    survey1response["1"], survey2response["2"], survey3response["3"])
                rID, PIN = CreateService.handle(
                    {**survey1response, **survey2response, **survey3response}, MessengerView.handlePI(params))
                fulfillmentText["fulfillmentMessages"] = message["fulfillmentMessages"]
                fulfillmentText["fulfillmentMessages"][1]["text"]["text"][0] = str(
                    fulfillmentText["fulfillmentMessages"][1]["text"]["text"][0]).format(rID, PIN, params["mobileNum"], EMAIL, HOTLINE)
                return fulfillmentText
            except IncorrectResponse as e:
                fulfillmentText["fulfillmentMessages"][0]["text"]["text"].append(
                    str(e))
                return fulfillmentText
            except IncompleteResponse as e:
                fulfillmentText["fulfillmentMessages"][0]["text"]["text"].append(
                    str(e))
                return fulfillmentText
            except Exception as e:
                print(e)
                fulfillmentText["fulfillmentMessages"][0]["text"]["text"].append(
                    "Our deepest apologies, our servers encountered an error. Please try again later.")
                return fulfillmentText
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def handlePI(params: dict):
        name = params["name"].split(
            ", ") if ", " in params["name"] else params["name"].split(",")
        return {"first_name": name[1], "middle_name": name[2], "last_name": name[0], "birthdate": params["birthDate"], "sex": params["sex"], "occupation": params["occupation"], "email": params["email"] if params["email"] != "N/A" else "", "mobile_number": params["mobileNum"], "home_address": params["homeAddress"], "municipality": params["municipality"], "barangay": params["barangay"], "province": params["province"], "region": params["region"]}

    def checkResponse(survey1response: str, survey2response: str, survey3response: str):
        reformedS1 = survey1response.upper()
        reformedS2 = survey2response.upper()
        reformedS3 = survey3response.upper()
        statsS1 = (len(re.findall("[0-9]{1,2}\.?\s(Y|N)", reformedS1)),
                   len(re.findall("[^YN\s\n\.0-9]", reformedS1)))
        statsS2 = (len(re.findall("[0-9]{1,2}\.?\s(Y|N|U)", reformedS2)),
                   len(re.findall("[^YN\s\n\.0-9]", reformedS2)))
        statsS3 = (len(re.findall("[0-9]{1,2}\.?\s(Y|N)", reformedS3)),
                   len(re.findall("[^YN\s\n\.0-9]", reformedS3)))
        if statsS1[0] != surveyFormConfig["lengthS1"] or statsS2[0] != surveyFormConfig["lengthS2"] or statsS3[0] != surveyFormConfig["lengthS3"]:
            raise IncompleteResponse(
                surveyFormConfig["lengthS1"] - statsS1[0], surveyFormConfig["lengthS2"] - statsS2[0], surveyFormConfig["lengthS3"] - statsS3[0])
        if statsS1[1] != 0 or statsS2[1] != 0 or statsS3[1] != 0:
            raise IncorrectResponse

    def confirmMobileNumber(mobileNum: str):
        try:
            mn_entry = TABLES["AM"].objects.get(
                pk=int(mobileNum.replace("+", "")))
            return mn_entry
        except ObjectDoesNotExist:
            return False
        except:
            return False
