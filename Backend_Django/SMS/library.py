from projectBakuna.environment import EMAIL, HOTLINE, NAME, globeConfig

defaultResponse = {
    "defaultWelcome": "Text \"APPLY\" to to %(virtual_number_1)s for non-Globe subscribers and %(virtual_number_2)s for Globe subscribers to begin your Covid-19 Vaccination Application. If you have already applied, text \"STATUS <Reference ID> <PIN>\" to %(virtual_number_1)s for non-Globe subscribers and %(virtual_number_2)s for Globe subscribers to check the status of your application. For other concerns, please contact us via our email: %(email)s or our hotline: %(hotline)s." % {'virtual_number_1': globeConfig.get("shortCodeCrossTelco"), 'virtual_number_2': globeConfig.get("shortCode"), 'email': EMAIL, 'hotline': HOTLINE},
    "defaultVerify": "'%(name)s' woud like to access your account, enter the confirmation code to proceed: {}" % {'name': NAME},
    "defaultEligibilityNotification": "Greetings {}, your Covid-19 vaccine application is {} as reviewed by your assigned medical personnel. Please text \"STATUS <Reference ID>\" to %(virtual_number_1)s for non-Globe subscribers and %(virtual_number_2)s for Globe subscribers to get more information." % {'virtual_number_1': globeConfig.get("shortCodeCrossTelco"), 'virtual_number_2': globeConfig.get("shortCode")},
    "defaultStatusCheck": "Greetings {}, the eligibility status of your Covid-19 vaccine application is {} due to the following:\n\n\"{}\",\n\nas pointed out by your assigned medical personnel. If you have any issues or concerns, please do reach us at our email: %(email)s or our hotline: %(hotline)s" % {'email': EMAIL, 'hotline': HOTLINE},
    "defaultSessionNotification": "",
    "defaultSessionConfirmation": "",
    "defaultSessionChangeNotification": "",
    "errorID": "Sorry, it seems like this reference ID does not belong to your mobile number or does not exist at all. Please check your Reference ID if it is correct and try again.",
    "errorPIN": "Sorry it seems like this PIN is incorrect. Please check your reference ID and PIN and try again.",
    "defaultError": "Our deepest apologies, our servers encountered an error. Please try again later.",
    "invalidNum": "You gave us an {}. Provided numbers for SMS must be of mobile type.",
    "fallback": ["Sorry, we didn't quite catch that. Come again?", "It seems we can't recognize what you're saying. Can you try again?"]
}
