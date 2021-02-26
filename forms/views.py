import json
from django.http.response import HttpResponse
from rest_framework import status
from FORMS.serializers import AuthMobileNumberSerializer, PersonalInformationSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.views import View


class FormsView(View):

    @require_POST
    @csrf_exempt
    def postRequest(request):
        if request.method == 'POST' and request.get_host() == '127.0.0.1:8000' and request.content_type == 'application/json':
            dataQuery = json.loads(request.body)
            try:
                mn_serializer = AuthMobileNumberSerializer(
                    data={
                        "mobile_number": dataQuery["mobile_number"],
                    }
                )
                if mn_serializer.is_valid():
                    mn_serializer.create(mn_serializer.validated_data)
                    serializer = PersonalInformationSerializer(data=dataQuery)
                    if serializer.is_valid():
                        serializer.create(serializer.validated_data)
                        return HttpResponse(status=status.HTTP_201_CREATED)
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            except:
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
