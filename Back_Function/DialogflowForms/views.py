from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import requests
import json
import os
from .SaveConversation import conversations
from .CheckForms import check


# define home function
def home(request):
    return HttpResponse('Hello World!')

@csrf_exempt
def webhook(request):
    req = json.loads(request.body)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = JsonResponse(res, safe = False)
    return r

def processRequest(req):
    log = Conversations.Log()
    smsForm = check.SmsForm()
    messengerForm = check.MessengerForm()
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")

    if intent == 'Save SMS Form':
        personalInfo = parameters.get("personalInfo")
        survey1 = parameters.get("survey1response")
        survey2 = parameters.get("survey2response")

        if messengerForm.isCorrect(survey1,survey2) == False: 
            webhookResponse = "Sorry, your response has not been save. It seems like have a typo in your response. Please enter 'save form' to restart the process."
            return {

                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                webhookResponse
                            ]

                        }
                    }
                ]
            }


        if smsForm.isComplete(personalInfo,survey1,survey2) == False:
            personaInfoNumberOfResponse = checker.numberOfAnswers(personalInfo)
            s1NumberOfResponse = smsForm.numberOfAnswers(survey1)
            s2NumberOfResponse = smsForm.numberOfAnswers(survey2)
            webhookResponse = "Sorry, your response has not been saved. It seems like you have not answered all the questions in the survey. It seems like you answered " + str(personaInfoNumberOfResponse) + "from your personal info form, " +  str(s1NumberOfResponse) + " answer/s from survey 1, and " + str(s2NumberOfResponse) + " answer/s from survey 2. Please enter 'save form' again to restart the process."

            return {

                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                webhookResponse
                            ]

                        }
                    }
                ]
            }

        info = [personalInfo, survey1, survey2]
        log.saveSMSForms(sessionID, info, intent)

    if intent == 'Save Messenger Form': 
        firstName = parameters.get("firstName")
        middleName = parameters.get("middleName")
        lastName = parameters.get("lastName")
        birthDate = parameters.get("birthDate")
        sex = parameters.get("sex")
        mobileNum = parameters.get("mobileNum")
        homeAddress = parameters.get("homeAddress")
        city = parameters.get("city")
        barangay = parameters.get("barangay")
        survey1 = parameters.get("survey1response")
        survey2 = parameters.get("survey2response")


        if messengerForm.isCorrect(survey1,survey2) == False: 
            webhookResponse = "Sorry, your response has not been save. It seems like have a typo in your response. Please enter 'save form' to restart the process."
            return {

                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                webhookResponse
                            ]

                        }
                    }
                ]
            }

        if messengerForm.isComplete(survey1,survey2) == False:
            s1NumberOfResponse = messengerForm.numberOfAnswers(survey1)
            s2NumberOfResponse = messengerForm.numberOfAnswers(survey2)
            webhookResponse = "Sorry, your response has not been saved. It seems like you have not answered all the questions in the survey. It seems like you only got " +  str(s1NumberOfResponse) + " answer/s from survey 1 and " + str(s2NumberOfResponse) + " answer/s from survey 2. Please enter 'save form' again to restart the process."
            return {

                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                webhookResponse
                            ]

                        }
                    }
                ]
            }

        info = [firstName, middleName, lastName, birthDate, sex, mobileNum, homeAddress, city, barangay, survey1, survey2]
        log.saveMessengerForms(sessionID, info, intent)




                                             