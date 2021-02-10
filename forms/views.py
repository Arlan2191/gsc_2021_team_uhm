import json
from rest_framework import status
from forms.serializers import AuthMobileNumberSerializer, PersonalInformationSerializer
from forms.models import Eligibility_Status, Personal_Information, Tracking_Information
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.views import View


class FormsView(View):

    @require_GET
    @csrf_exempt
    def getRequest(request, table_name, id=0):
        if request.method == 'GET' and request.get_host() == "127.0.0.1:8000":
            try:
                dataQuery = {}
                if table_name == "PI":
                    if id != 0:
                        dataQuery = [Personal_Information.objects.get(id=id)]
                    else:
                        dataQuery = Personal_Information.objects.all()
                if table_name == "ES":
                    if id != 0:
                        dataQuery = [Eligibility_Status.objects.get(id=id)]
                    else:
                        dataQuery = Eligibility_Status.objects.all()
                if table_name == "TI":
                    if id != 0:
                        dataQuery = [Tracking_Information.objects.get(id=id)]
                    else:
                        dataQuery = Tracking_Information.objects.all()
                serializer = serialize('json', dataQuery)
                return JsonResponse({"HTTPStatus": serializer}, safe=False, status=status.HTTP_200_OK)
            except Exception as e:
                return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_400_BAD_REQUEST)

    @require_POST
    @csrf_exempt
    def postRequest(request):
        dataQuery = json.loads(request.body)
        try:
            serializer = AuthMobileNumberSerializer(
                data={
                    "mobile_number": dataQuery["mobile_number"],
                    "amount_entry": FormsView.__retrieveEntriesLength(dataQuery) + 1,
                }
            )
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
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

    def __retrieveEntriesLength(dataQuery):
        entries = len(Personal_Information.objects.filter(
            mobile_number=dataQuery["mobile_number"]))
        if entries <= 9:
            return entries
        raise Exception("Maximum entries for given mobile number")

    def __OTPAuthentication():  # TODO
        pass
