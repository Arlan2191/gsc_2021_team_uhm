from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error
    }
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    response.data = {
        'errors': response.data
    }

    return response


class ConfirmationException(Exception):
    def __str__(self) -> str:
        return "You are not yet scheduled an appointment for you to confirm."

class SubscriptionException(Exception):
    def __str__(self) -> str:
        return "Your mobile number is neither verified nor subscribed."

class IncorrectPINException(Exception):
    def __str__(self) -> str:
        return "Incorrect PIN"

class InvalidUserType(Exception):
    def __str__(self) -> str:
        return "Invalid User Type"


class MaxEntryException(Exception):
    def __str__(self) -> str:
        return "Maximum entries (total of 10) attained for this mobile number. We will not receive anymore entries from this number."


class InvalidNumber(Exception):
    def __str__(self) -> str:
        return "Invalid Mobile Number"


class IncorrectResponse(Exception):
    def __str__(self) -> str:
        return "Sorry, your response has not been save. It seems like you provided an invalid choice in one of the medical history forms. Please enter 'REAPPLY' to restart the process."


class IncompleteResponse(Exception):
    def __init__(self, s1Num, s2Num, s3Num) -> None:
        self.__s1Num = s1Num
        self.__s2Num = s2Num
        self.__s3Num = s3Num

    def __str__(self) -> str:
        return "Sorry, your response has not been saved. It seems like you have not answered all the questions in the survey. It seems like you only missed {} question/s from survey 1, {} question/s from survey 2, and {} question/s from survey 3. Please enter 'REAPPLY' again to restart the process.".format(self.__s1Num, self.__s2Num, self.__s3Num)
