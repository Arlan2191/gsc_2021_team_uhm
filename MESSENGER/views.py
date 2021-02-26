from django.views.decorators.http import require_POST
from FORMS.serializers import PersonalInformationSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.views import View
from projectBakuna.environment import surveyMessengerFormConfig
from projectBakuna.exceptions import IncompleteResponse, IncorrectResponse
import re
import json


class MessengerView(View):

    @require_POST
    @csrf_exempt
    def postRequest(request):
        try:
            message = json.loads(request.body)
            dialogFlowResponse = MessengerView.processMessage(message=message)
            return JsonResponse(dialogFlowResponse, safe=False)
        except:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def processMessage(self, message: dict):
        sessionID = message["responseId"]
        result = message["queryResult"]
        intent = message["intent"]["displayName"]
        queryText = message["queryText"]
        params = message["parameters"]
        survey1response = {"1": params.pop("survey1response")}
        survey2response = {"2": params.pop("survey2response")}
        fulfillmentText = {"fulfillmentMessages": [{"text": {"text": []}}]}

        if intent == "Save Messenger Form":
            try:
                self.checkResponse(survey1response, survey2response)
                serializer = PersonalInformationSerializer(data=params)
                if serializer.is_valid():
                    serializer.create(serializer.validated_data)
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            except IncorrectResponse as e:
                fulfillmentText["fulfillmentMessages"][0]["text"]["text"].append(
                    str(e))
                return fulfillmentText
            except IncompleteResponse as e:
                fulfillmentText["fulfillmentMessages"][0]["text"]["text"].append(
                    str(e))
                return fulfillmentText
            except:
                fulfillmentText["fulfillmentMessages"][0]["text"]["text"].append(
                    "Our deepest apologies, our servers encountered an error. Please try again later.")
                return fulfillmentText

    def checkResponse(survey1response: str, survey2response: str):
        reformedS1 = survey1response.upper()
        reformedS2 = survey2response.upper()
        statsS1 = (len(re.findall("[0-9]{1,2}\.?\s(Y|N)", reformedS1)),
                   len(re.findall("[^YN\s\n\.0-9]", reformedS1)))
        statsS2 = (len(re.findall("[0-9]{1,2}\.?\s(Y|N)", reformedS2)),
                   len(re.findall("[^YN\s\n\.0-9]", reformedS2)))
        if statsS1[0] != surveyMessengerFormConfig["lengths1"] or statsS2[0] != surveyMessengerFormConfig["lengths2"]:
            raise IncompleteResponse(
                surveyMessengerFormConfig["lengths1"] - statsS1, surveyMessengerFormConfig["lengths2"] - statsS2)
        if statsS1[1] != 0 or statsS2[1] != 0:
            raise IncorrectResponse
