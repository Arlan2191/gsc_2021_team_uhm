import json
from rest_framework import status
from forms.serializers import AuthMobileNumberSerializer, PersonalInformationSerializer
from forms.models import Personal_Information
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.views import View


class FormsView(View):

    @require_POST
    @csrf_exempt
    def postRequest(request):
        if request.method == 'POST' and request.get_host() == "127.0.0.1:8000" and request.content_type == 'application/json':
            dataQuery = json.loads(request.body)
            try:
                mn_serializer = AuthMobileNumberSerializer(
                    data={
                        "mobile_number": dataQuery["mobile_number"],
                        "amount_entry": FormsView.__retrieveEntriesLength(dataQuery) + 1,
                    }
                )
                if mn_serializer.is_valid():
                    mn_serializer.create(mn_serializer.validated_data)
                    serializer = PersonalInformationSerializer(data=dataQuery)
                    if serializer.is_valid():
                        serializer.create(serializer.validated_data)
                        return JsonResponse({"HTTPStatus": "Succesfully added onto database"}, safe=False, status=status.HTTP_201_CREATED)
                    return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist as e:
                return JsonResponse({"HTTPStatus": str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_400_BAD_REQUEST)

    def __retrieveEntriesLength(dataQuery):
        entries = len(Personal_Information.objects.filter(
            mobile_number=dataQuery["mobile_number"]))
        if entries <= 9:
            return entries
        raise Exception("Maximum entries for given mobile number")

    def __OTPAuthentication():  # TODO
        pass
