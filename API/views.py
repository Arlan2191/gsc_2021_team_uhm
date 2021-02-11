from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.serializers import Serializer
from FORMS.models import Personal_Information
from API.serializers import EligibilityStatusSerializer, TrackingInformationSerializer, VaccinationSiteSerializer
from API.models import Eligibility_Status, Tracking_Information, Vaccination_Site
from django.core.serializers import serialize
from django.http import JsonResponse
from django.views import View
from rest_framework import status


class ApiView(View):

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
                if table_name == "VS":
                    if id != 0:
                        dataQuery = list(
                            Vaccination_Site.objects.filter(vs_id=id))
                    else:
                        dataQuery = Vaccination_Site.objects.all()
                serializer = serialize('json', dataQuery)
                return JsonResponse({"HTTPStatus": serializer}, safe=False, status=status.HTTP_200_OK)
            except Exception as e:
                return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_400_BAD_REQUEST)

    @require_POST
    @csrf_exempt
    def postRequest(request, table_name):
        if request.method == 'POST' and request.get_host() == "127.0.0.1:8000" and request.content_type == 'multipart/form-data':
            try:
                dataQuery = ApiView.__formHander(dict(request.POST))
                serializer = None
                if table_name == 'VS':
                    serializer = VaccinationSiteSerializer(data=dataQuery)
                if table_name == 'TI':
                    serializer = TrackingInformationSerializer(data=dataQuery)
                if table_name == 'ES':
                    serializer = EligibilityStatusSerializer(data=dataQuery)
                if serializer.is_valid():
                    serializer.create(serializer.validated_data)
                    return JsonResponse({"HTTPStatus": "Successfully added onto database"}, safe=False, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({"HTTPStatus": "Bad Request"}, safe=False, status=status.HTTP_404_NOT_FOUND)

    def __formHander(postRequest: dict):
        validQuery = {}
        for key, value in zip(postRequest.keys(), postRequest.values()):
            validQuery[key] = value[0]
        return validQuery
